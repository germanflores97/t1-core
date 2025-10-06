from fastapi import HTTPException
from src.commons.models import PyObjectId
from src.tarjetas.schemas import CrearTarjetaRequest, CrearTarjetaResponse, ConsultarTarjetaResponse, ActualizarTarjetaRequest, ActualizarTarjetaResponse, EliminarTarjetaResponse
from src.tarjetas.models import Tarjeta
from src.tarjetas.utils import ofuscar_tarjeta
from src.commons.exceptions import BusinessException
import src.tarjetas.repository as tarjetas_repository 
import src.clientes.repository as clientes_repository

from typing import Tuple
from datetime import datetime

def crear_tarjeta(datos_tarjeta: CrearTarjetaRequest) -> Tuple[bool, CrearTarjetaResponse]:
    """
        <p>
        Devuelve como resultado una tupla, la primer posicion es una bandera que indica si se registro correctamente el
        registtro, el segundo parametro es la respuesta del servicio.
        </p>
    """
    cliente = clientes_repository.consultar_cliente(datos_tarjeta.cliente_id)
    if not cliente:
        raise HTTPException(404, "Cliente no existente")

    tarjeta_ofuscada = ofuscar_tarjeta(datos_tarjeta.numero_tarjeta)
    bin = datos_tarjeta.numero_tarjeta[0:8]
    terminacion = datos_tarjeta.numero_tarjeta[12:]

    tarjeta_existente = tarjetas_repository.consultar_tarjeta_por_cliente_id_bin_terminacion(datos_tarjeta.cliente_id, bin, terminacion)
    if tarjeta_existente:
        return False, CrearTarjetaResponse(id=str(tarjeta_existente.get("_id")))
    
    tarjeta_id = tarjetas_repository.crear_tarjeta(
        Tarjeta(
            cliente_id=cliente["_id"], numero_tarjeta=tarjeta_ofuscada, cvv=datos_tarjeta.cvv,
            expiracion=datos_tarjeta.expiracion, activa=True, bin=bin, terminacion=terminacion, fecha_creacion=datetime.now()
        )
    )
    
    return True, CrearTarjetaResponse(id=str(tarjeta_id))

def consultar_tarjeta(id:str) -> ConsultarTarjetaResponse:
    tarjeta = tarjetas_repository.consultar_tarjeta(id)
    if not tarjeta:
        raise BusinessException(mensaje="Registro no encontrado", codigo=404)
    
    tarjeta["fecha_creacion"] = tarjeta.pop("fecha_creacion").strftime("%Y/%m/%d %H:%M:%S")
    if tarjeta["fecha_actualizacion"]:
        tarjeta["fecha_actualizacion"] = tarjeta.pop("fecha_actualizacion").strftime("%Y/%m/%d %H:%M:%S")
    
    tarjeta["id"] = str(tarjeta.pop("_id"))
    tarjeta["cliente_id"] = str(tarjeta.pop("cliente_id"))
    
    return ConsultarTarjetaResponse(**tarjeta)

def actualizar_tarjeta(id: str, datos_tarjeta: ActualizarTarjetaRequest) -> ActualizarTarjetaResponse:
    cliente = clientes_repository.consultar_cliente(datos_tarjeta.cliente_id)
    if not cliente:
        raise HTTPException(404, "Cliente no existente")
    
    #Se setean datos vacios solo para que se cumpla el contrato, el resto no se actualiza desde el query
    registros_actualizados = tarjetas_repository.actualizar_tarjeta(
        Tarjeta(
            _id=PyObjectId(id), cliente_id=cliente["_id"], numero_tarjeta="", cvv=datos_tarjeta.cvv, expiracion="",
            activa=datos_tarjeta.activa, bin="", terminacion="", fecha_actualizacion=datetime.now()
        )
    )
    if registros_actualizados == 0:
        raise BusinessException(mensaje="Registro no encontrado", codigo=404)
    
    return ActualizarTarjetaResponse(actualizada=True)

def eliminar_tarjeta(id:str) -> EliminarTarjetaResponse:
    registros_eliminados = tarjetas_repository.eliminar_tarjeta(id)

    if registros_eliminados == 0:
        raise BusinessException(mensaje="Registro no encontrado", codigo=404)
    
    return EliminarTarjetaResponse(eliminada=True)