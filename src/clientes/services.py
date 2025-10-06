from src.commons.exceptions import BusinessException
from src.clientes.schemas import CrearClienteRequest, CrearClienteResponse, ActualizarClienteRequest, ActualizarClienteResponse, ConsultarClienteResponse, EliminarClienteResponse
from src.clientes.models import Cliente
import src.clientes.repository as clientes_repository
from datetime import datetime

from typing import Tuple

def crear_cliente(cliente: CrearClienteRequest) -> Tuple[bool, CrearClienteResponse]:
    """
        <p>
        Devuelve como resultado una tupla, la primer posicion es una bandera que indica si se registro correctamente el
        registtro, el segundo parametro es la respuesta del servicio.
        </p>
    """
    cliente_existente = clientes_repository.consultar_cliente_por_curp(cliente.curp)
    if cliente_existente: #Convierte a idempotente el endpoint
        return False, CrearClienteResponse(id=str(cliente_existente.get("_id")))
    
    id_cliente = clientes_repository.crear_cliente(
        Cliente(
            nombres=cliente.nombres, apellido_paterno=cliente.apellido_paterno, apellido_materno=cliente.apellido_materno,
            curp=cliente.curp, email=cliente.email, telefono=cliente.telefono, activo=True, fecha_creacion=datetime.today()
        )
    )

    return True, CrearClienteResponse(id=id_cliente)

def actualizar_cliente(id:str, cliente: ActualizarClienteRequest) -> ActualizarClienteResponse:
    registros_actualizados = clientes_repository.actualizar_cliente(
        Cliente(
            _id=id, nombres=cliente.nombres, apellido_paterno=cliente.apellido_paterno, apellido_materno=cliente.apellido_materno,
            curp=cliente.curp, email=cliente.email, telefono=cliente.telefono, activo=cliente.activo, fecha_actualizacion=datetime.today()
        )
    )

    if registros_actualizados == 0:
        raise BusinessException(mensaje="Registro no encontrado", codigo=404)

    return ActualizarClienteResponse(actualizado=True)

def consultar_cliente(id:str) -> ConsultarClienteResponse:
    cliente = clientes_repository.consultar_cliente(id)
    if not cliente:
        raise BusinessException(mensaje="Registro no encontrado", codigo=404)
    
    cliente["id"] = str(cliente.pop("_id"))
    cliente["fecha_creacion"] = cliente.pop("fecha_creacion").strftime("%Y/%m/%d %H:%M:%S")
    if cliente["fecha_actualizacion"]:
        cliente["fecha_actualizacion"] = cliente.pop("fecha_actualizacion").strftime("%Y/%m/%d %H:%M:%S")
    
    return ConsultarClienteResponse(**cliente)

def eliminar_cliente(id:str) -> EliminarClienteResponse:
    registros_eliminados = clientes_repository.eliminar_cliente(id)

    if registros_eliminados == 0:
        raise BusinessException(mensaje="Registro no encontrado", codigo=404)
    
    return EliminarClienteResponse(eliminado=True)