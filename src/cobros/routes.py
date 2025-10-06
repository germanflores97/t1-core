from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse

from src.commons.schemas import GenericResponse
from src.cobros.schemas import AplicarCobroRequest, AplicarCobroResponse, ConsultarHistorialPorClienteResponse
import src.cobros.services as cobros_services

cobros_router = APIRouter()

@cobros_router.post("/", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[AplicarCobroResponse])
def aplicar_cobro(request: AplicarCobroRequest):
    response = cobros_services.aplicar_cobro(request)
    codigo, mensaje = (200, "Cobro aplicado correctamente") if response.aplicado else (400, "Cobro no aplicado")

    return JSONResponse(GenericResponse(mensaje=mensaje, respuesta=response).model_dump(), status_code=codigo)

@cobros_router.get("/{id}", tags=["Cobros"], response_class=JSONResponse, response_model=GenericResponse[ConsultarHistorialPorClienteResponse])
def consultar_historial_por_cliente(id:str = Path(min_length=24, max_length=24)):
    response = cobros_services.consultar_historial_por_cliente(id)

    return JSONResponse(GenericResponse(mensaje="Consulta realizada correctamente", respuesta=response).model_dump(), status_code=200)