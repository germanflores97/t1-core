from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse

from src.commons.schemas import GenericResponse
from src.tarjetas.schemas import CrearTarjetaRequest, CrearTarjetaResponse, ConsultarTarjetaResponse, ActualizarTarjetaRequest, ActualizarTarjetaResponse, EliminarTarjetaResponse
import src.tarjetas.services as tarjetas_services

tarjetas_router = APIRouter()

@tarjetas_router.post("/", tags=["Tarjetas"], response_class=JSONResponse, response_model=GenericResponse[CrearTarjetaResponse])
def crear_tarjeta(request: CrearTarjetaRequest):
    """
        <p>Permite la creacion de una tarjeta asociada a un cliente.</p>
        <p><b>Importante</b>: En este servicio se hace la validacion de Luhn para validar que la tarjeta sea correcta.</p>
        <p>
        <b>Importante</b>: En caso que el registro por cliente_id, bin y terminacion no exista, se almacenara y se devolvera
        un HTTP Code 201 con el ID generado, en caso que ya exista con los 3 criterios, simplemente se regresara un HTTP Code 200
        y el ID del registro persistido.
        </p>
    """
    registrada, response = tarjetas_services.crear_tarjeta(request)
    codigo, mensaje = (201, "Tarjeta registrada correctamente") if registrada else (200, "La tarjeta ya ha sido registrada")

    return JSONResponse(GenericResponse(mensaje=mensaje, respuesta=response).model_dump(), status_code=codigo)

@tarjetas_router.get("/{id}", tags=["Tarjetas"], response_class=JSONResponse, response_model=GenericResponse[ConsultarTarjetaResponse])
def consultar_tarjeta(id:str = Path(min_length=24, max_length=24)):
    """
        <p>Permite la consulta de una tarjeta por su ID.</p>
    """
    response = tarjetas_services.consultar_tarjeta(id)

    return JSONResponse(GenericResponse(mensaje="Consulta realizada correctamente", respuesta=response).model_dump(), status_code=200)

@tarjetas_router.put("/{id}", tags=["Tarjetas"], response_class=JSONResponse, response_model=GenericResponse[ActualizarTarjetaResponse])
def actualizar_tarjeta(request: ActualizarTarjetaRequest, id:str = Path(min_length=24, max_length=24)):
    """
        <p>Permite la actualizacion de una tarjeta por su ID.</p>
    """
    response = tarjetas_services.actualizar_tarjeta(id, request)

    return JSONResponse(GenericResponse(mensaje="Registro actualizado correctamente", respuesta=response).model_dump(), status_code=200)

@tarjetas_router.delete("/{id}", tags=["Tarjetas"], response_class=JSONResponse, response_model=GenericResponse[EliminarTarjetaResponse])
def eliminar_tarjeta(id:str = Path(min_length=24, max_length=24)):
    """
        <p>Permite la eliminacion de una tarjeta por su ID.</p>
    """
    response = tarjetas_services.eliminar_tarjeta(id)

    return JSONResponse(GenericResponse(mensaje="Registro eliminado correctamente", respuesta=response).model_dump(), status_code=200)