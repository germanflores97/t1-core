from datetime import datetime, timedelta, timezone
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError, ExpiredSignatureError

from src.commons.schemas import GenericResponse
from src.cobros.schemas import AplicarCobroRequest, AplicarCobroResponse, ConsultarHistorialPorClienteResponse, AplicarReembolsoResponse
import src.cobros.services as cobros_services
from src.core.settings import configs 



cobros_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer("/cobros/auth/")

def encode_token(payload:Dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=configs().oauth2_minutes_expires)
    payload.update({"exp": expire})
    token = jwt.encode(payload, configs().oauth2_password, algorithm="HS256")
    return token

def decode_token(token:Annotated[str, Depends(oauth2_scheme)]) -> Dict:
    try:
        data = jwt.decode(token, configs().oauth2_password, algorithms=["HS256"])
        return {"username": data["username"], "password": configs().oauth2_password}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@cobros_router.post("/auth/", tags=["Cobros"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
        <p>Genera un JWT y da la capacidad de implementar el estandar oauth2 para la autenticacion de los servicios.</p>
        <p><b>Importante</b>: Se configuro una expiracion de 5 minutos.</p>
        <p><b>Importante</b>: De momento no se hace un validacion de rol, solo que las credenciales para generar el token sean correctas.</p>
    """
    user = {"username": configs().oauth2_user, "password": configs().oauth2_password}
    if form_data.username != user["username"] or form_data.password != user["password"]:
        raise HTTPException(400, "Usuario o password incorrectos")

    token = encode_token({"username": user["username"]})
    return {"access_token": token}

@cobros_router.post("/", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[AplicarCobroResponse])
def aplicar_cobro(request: AplicarCobroRequest):
    """
        <p>Permite aplicar un cobro a una tarjeta.<p>
        <p>Tambien se almacenan cobros rechazados con un estatus de aplicado en false.</p>
    """
    response = cobros_services.aplicar_cobro(request)
    codigo, mensaje = (200, "Cobro aplicado correctamente") if response.aplicado else (400, "Cobro no aplicado")

    return JSONResponse(GenericResponse(mensaje=mensaje, respuesta=response).model_dump(), status_code=codigo)

@cobros_router.post("/v2/", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[AplicarCobroResponse])
def aplicar_cobro_v2(request: AplicarCobroRequest, user: Annotated[dict, Depends(decode_token)]):
    """
        <p>Permite aplicar un cobro a una tarjeta utilizando autenticacion con JWT y oauth2.<p>
        <p>Tambien se almacenan cobros rechazados con un estatus de aplicado en false.</p>
        <p><b>Importante</b>: Se debe agregar el JWT con autenticacion <b>bearer</b> para consumirlo.</p>
    """
    return aplicar_cobro(request)

@cobros_router.get("/{id}", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[ConsultarHistorialPorClienteResponse])
def consultar_historial_por_cliente(id:str = Path(min_length=24, max_length=24)):
    """
        <p>Permite consultar el historial de cobros por cliente_id.</p>
    """
    response = cobros_services.consultar_historial_por_cliente(id)

    return JSONResponse(GenericResponse(mensaje="Consulta realizada correctamente", respuesta=response).model_dump(), status_code=200)

@cobros_router.post("/{id}/reembolso/", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[AplicarReembolsoResponse])
def aplicar_reembolso(id:str = Path(min_length=24, max_length=24)):
    """
        <p>Permite aplicar un reembolso a un cobro previamente aplicado.</p>
        <p><b>Importante</b>: Solo se puede hacer reembolso a cobros aplicados y que no hayan sido reembolsados previamente.</p>
    """
    response = cobros_services.aplicar_reembolso(id)
    codigo, mensaje = (200, "Reembolso aplicado correctamente") if response.reembolsado else (400, "Reembolso no aplicado")

    return JSONResponse(GenericResponse(mensaje=mensaje, respuesta=response).model_dump(), status_code=codigo)

@cobros_router.post("/v2/{id}/reembolso/", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[AplicarReembolsoResponse])
def aplicar_reembolso_v2(user: Annotated[dict, Depends(decode_token)], id:str = Path(min_length=24, max_length=24)):
    """
        <p>Permite aplicar un reembolso a un cobro previamente aplicado utilizando autenticacion con JWT y oauth2.</p>
        <p><b>Importante</b>: Solo se puede hacer reembolso a cobros aplicados y que no hayan sido reembolsados previamente.</p>
        <p><b>Importante</b>: Se debe agregar el JWT con autenticacion <b>bearer</b> para consumirlo.</p>
    """
    return aplicar_reembolso(id)