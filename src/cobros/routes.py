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
    user = {"username": configs().oauth2_user, "password": configs().oauth2_password}
    if form_data.username != user["username"] or form_data.password != user["password"]:
        raise HTTPException(400, "Usuario o password incorrectos")

    token = encode_token({"username": user["username"]})
    return {"access_token": token}

@cobros_router.post("/", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[AplicarCobroResponse])
def aplicar_cobro(request: AplicarCobroRequest):
    response = cobros_services.aplicar_cobro(request)
    codigo, mensaje = (200, "Cobro aplicado correctamente") if response.aplicado else (400, "Cobro no aplicado")

    return JSONResponse(GenericResponse(mensaje=mensaje, respuesta=response).model_dump(), status_code=codigo)

@cobros_router.post("/v2/", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[AplicarCobroResponse])
def aplicar_cobro_v2(request: AplicarCobroRequest, user: Annotated[dict, Depends(decode_token)]):
    return aplicar_cobro(request)

@cobros_router.get("/{id}", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[ConsultarHistorialPorClienteResponse])
def consultar_historial_por_cliente(id:str = Path(min_length=24, max_length=24)):
    response = cobros_services.consultar_historial_por_cliente(id)

    return JSONResponse(GenericResponse(mensaje="Consulta realizada correctamente", respuesta=response).model_dump(), status_code=200)

@cobros_router.post("/{id}/reembolso/", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[AplicarReembolsoResponse])
def aplicar_reembolso(id:str = Path(min_length=24, max_length=24)):
    response = cobros_services.aplicar_reembolso(id)
    codigo, mensaje = (200, "Reembolso aplicado correctamente") if response.reembolsado else (400, "Reembolso no aplicado")

    return JSONResponse(GenericResponse(mensaje=mensaje, respuesta=response).model_dump(), status_code=codigo)

@cobros_router.post("/v2/{id}/reembolso/", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[AplicarReembolsoResponse])
def aplicar_reembolso_v2(user: Annotated[dict, Depends(decode_token)], id:str = Path(min_length=24, max_length=24)):
    return aplicar_reembolso(id)