from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse

from src.commons.schemas import GenericResponse
from src.clientes.schemas import CrearClienteRequest, CrearClienteResponse, ActualizarClienteRequest, ActualizarClienteResponse, ConsultarClienteResponse, EliminarClienteResponse
import src.clientes.services as clientes_services

clientes_router = APIRouter()

@clientes_router.post("/", tags=["Clientes"], response_class=JSONResponse, response_model=GenericResponse[CrearClienteResponse])
def crear_cliente(request: CrearClienteRequest):
    """
        <p>
        <b>Importante</b>: En caso que el registro por CURP no exista, se almacenara y se devolvera
        un HTTP Code 201 con el ID generado, en caso que ya exista simplemente se regresara un HTTP Code 200
        y el ID del registro persistido.
        </p>
        <p>Permite la creacion de un cliente.</p>
    """
    registrado, response = clientes_services.crear_cliente(request)
    codigo, mensaje = (201, "Cliente registrado correctamente") if registrado else (200, "El cliente ya ha sido registrado")

    return JSONResponse(GenericResponse(mensaje=mensaje, respuesta=response).model_dump(), status_code=codigo)

@clientes_router.get("/{id}", tags=["Clientes"], response_class=JSONResponse, response_model=GenericResponse[ConsultarClienteResponse])
def consultar_cliente(id:str = Path(min_length=24, max_length=24)):
    response = clientes_services.consultar_cliente(id)
    
    return JSONResponse(GenericResponse(mensaje="Consulta realizada correctamente", respuesta=response).model_dump(), status_code=200)

@clientes_router.put("/{id}", tags=["Clientes"], response_class=JSONResponse, response_model=GenericResponse[ActualizarClienteResponse])
def actualizar_cliente(request: ActualizarClienteRequest, id:str = Path(min_length=24, max_length=24)):
    response = clientes_services.actualizar_cliente(id, request)

    return JSONResponse(GenericResponse(mensaje="Registro actualizado correctamente", respuesta=response).model_dump(), status_code=200)

@clientes_router.delete("/{id}", tags=["Clientes"], response_class=JSONResponse, response_model=GenericResponse[EliminarClienteResponse])
def eliminar_cliente(id:str = Path(min_length=24, max_length=24)):
    response = clientes_services.eliminar_cliente(id)

    return JSONResponse(GenericResponse(mensaje="Registro eliminado correctamente", respuesta=response).model_dump(), status_code=200)