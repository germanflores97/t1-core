from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import re

from src.commons.exceptions import BusinessException

FORMATO_FECHA_OPERACION = "%Y/%m/%d %H:%M:%S"

CVV_PATTERN = re.compile(r"^\d{3}$")

class AplicarCobroRequest(BaseModel):
    tarjeta_id: str = Field(min_length=24, max_length=24)
    importe: float
    fecha_operacion: str
    cvv: str
    concepto: Optional[str] = None

    @field_validator("fecha_operacion")
    def validar_fecha(cls, v):
        try:
            datetime.strptime(v, FORMATO_FECHA_OPERACION)
        except ValueError as error:
            raise BusinessException(codigo=422, mensaje="La fecha no tiene un formato de \"YYYY/MM/DD HH24:MI:SS\"")
        
        return v
    
    @field_validator("cvv")
    def validar_cvv(cls, v):
        if not CVV_PATTERN.match(v):
            raise BusinessException(codigo=422, mensaje="El CVV no tiene un formato correcto")
        
        return v

class AplicarCobroResponse(BaseModel):
    aplicado: bool
    detalle: str

class CobroDto(BaseModel):
    id: str
    tarjeta_id: str
    terminacion_tarjeta: str
    importe: float
    fecha_operacion: str
    concepto: Optional[str]
    aplicado: bool
    descripcion_estatus: str
    fecha_creacion: str
    fecha_actualizacion: Optional[str]
    reembolsado: bool
    fecha_reembolso: Optional[str]

class ConsultarHistorialPorClienteResponse(BaseModel):
    cobros: List[CobroDto]

class AplicarReembolsoResponse(BaseModel):
    reembolsado: bool
    detalle: str