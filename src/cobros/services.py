from datetime import datetime
from typing import Tuple
import time

from src.commons.exceptions import BusinessException
from src.commons.models import PyObjectId
from src.cobros.models import Cobro
from src.cobros.schemas import FORMATO_FECHA_OPERACION, AplicarCobroRequest, AplicarCobroResponse, CobroDto, ConsultarHistorialPorClienteResponse, AplicarReembolsoResponse
import src.tarjetas.repository as tarjetas_repository
import src.clientes.repository as clientes_repository
import src.cobros.repository as cobros_repository

def aplicar_cobro(cobro: AplicarCobroRequest) -> AplicarCobroResponse:
    valido, mensaje, tarjeta_id = validaciones_cobro(cobro)
    response = ejecutar_cobro(cobro) if valido else AplicarCobroResponse(aplicado=False, detalle=mensaje)

    response.id = cobros_repository.crear_cobro(
        Cobro(
            tarjeta_id=tarjeta_id, importe= cobro.importe, fecha_operacion=datetime.strptime(cobro.fecha_operacion, FORMATO_FECHA_OPERACION),
            concepto=cobro.concepto, estatus=response.aplicado, descripcion_estatus=response.detalle,
            fecha_creacion=datetime.now(), reembolsado=False
        )
    )

    return response

def validaciones_cobro(cobro: AplicarCobroRequest) -> Tuple[bool, str, PyObjectId]:
    tarjeta = tarjetas_repository.consultar_tarjeta(cobro.tarjeta_id)
    if not tarjeta:
        raise BusinessException(codigo=404, mensaje="Tarjeta no existente")
    if not tarjeta["activa"]:
        return False, "Tarjeta inactiva", tarjeta["_id"]

    cliente = clientes_repository.consultar_cliente(str(tarjeta["cliente_id"]))
    if not cliente:
        raise BusinessException(codigo=404, mensaje="Cliente no existente")
    if not cliente["activo"]:
        return False, "Cliente inactivo", tarjeta["_id"]
    
    if cobro.cvv != tarjeta["cvv"]:
        return False, "CVV incorrecto", tarjeta["_id"]
    
    mes, year = tarjeta["expiracion"].split("/")
    expiracion_numerico = int(f"{year}{mes}")
    fecha_actual_numerica = int(datetime.now().strftime("%y%m"))
    if expiracion_numerico < fecha_actual_numerica:
        return False, "Tarjeta ya expirada", tarjeta["_id"]
    
    return True, "", tarjeta["_id"]

def ejecutar_cobro(cobro: AplicarCobroRequest) -> AplicarCobroResponse:
    time.sleep(0.5) #Simula que se manda a llamar un servicio que ejecuta el cobro

    return AplicarCobroResponse(aplicado=True, detalle="Cobro aplicado correctamente")

def consultar_historial_por_cliente(id: str) -> ConsultarHistorialPorClienteResponse:
    cobros = []

    tarjetas_cliente = tarjetas_repository.consultar_tarjetas_por_cliente(id) #TODO: Optimizar serie de consultar en una sola llamada a base
    for datos_tarjeta in tarjetas_cliente:
        cobros_tarjeta = cobros_repository.consultar_cobros_por_tarjeta(tarjeta_id=datos_tarjeta["_id"])
        
        for cobro in cobros_tarjeta:
            cobros.append(
                CobroDto(
                    id=str(cobro["_id"]), tarjeta_id=str(datos_tarjeta["_id"]), terminacion_tarjeta=datos_tarjeta["terminacion"],
                    importe=cobro["importe"], fecha_operacion=cobro["fecha_operacion"].strftime(FORMATO_FECHA_OPERACION), concepto=cobro["concepto"],
                    aplicado=cobro["estatus"], descripcion_estatus=cobro["descripcion_estatus"], fecha_creacion=cobro["fecha_creacion"].strftime(FORMATO_FECHA_OPERACION),
                    fecha_actualizacion=cobro["fecha_actualizacion"].strftime(FORMATO_FECHA_OPERACION) if cobro["fecha_actualizacion"] else None,
                    reembolsado=cobro["reembolsado"], fecha_reembolso = cobro["fecha_reembolso"].strftime(FORMATO_FECHA_OPERACION) if cobro["fecha_reembolso"] else None
                )
            )

    return ConsultarHistorialPorClienteResponse(cobros=cobros)

def aplicar_reembolso(id:str) -> AplicarReembolsoResponse:
    valido, mensaje = validaciones_reembolso(id)
    response = ejecutar_reembolso(id) if valido else AplicarReembolsoResponse(reembolsado=False, detalle=mensaje)

    if response.reembolsado:
        cobros_repository.aplicar_reembolso(id)
    
    return response

def validaciones_reembolso(id:str) -> Tuple[bool, str]:
    cobro = cobros_repository.consultar_cobro(id)
    if not cobro:
        raise BusinessException(codigo=404, mensaje="Registro de cobro no existente")

    if cobro["reembolsado"]:
        return False, "Este cobro ya ha sido reembolsado"
    
    if not cobro["estatus"]:
        return False, f"El pago no fue generado y tiene un estatus: {cobro["descripcion_estatus"]}"
    
    return True, ""

def ejecutar_reembolso(id:str) -> AplicarReembolsoResponse:
    time.sleep(0.3)

    return AplicarReembolsoResponse(reembolsado=True, detalle="Reembolso aplicado correctamente")