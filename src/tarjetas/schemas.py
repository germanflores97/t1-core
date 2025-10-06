from pydantic import BaseModel, field_validator, Field
import re
from datetime import datetime
from typing import Optional

from src.commons.exceptions import BusinessException
from src.clientes.models import Cliente
from src.tarjetas.validations import LuhnValidations

NUMERO_TARJETA_PATTERN = re.compile(r"^\d{16}$")

CVV_PATTERN = re.compile(r"^\d{3}$")

EXPIRACION_PATTERN = re.compile(r"^(0[1-9]|1[0-2])\/(\d{2})$")

class CrearTarjetaRequest(BaseModel):
    cliente_id: str = Field(min_length=24, max_length=24)
    numero_tarjeta: str
    cvv: str
    expiracion: str

    @field_validator("numero_tarjeta")
    def validar_numero_tarjeta(cls, v):
        """
            <p>
            <b>Importante</b>: Este validador hace la validacion que la tarjeta tenga un formato correcto
            y cumpla la validacion de Luhn que se solicito
            </p>
        """
        if not NUMERO_TARJETA_PATTERN.match(v):
            raise BusinessException(codigo=422, mensaje="La tarjeta no tiene un formato correcto")

        if not LuhnValidations.is_luhn_valid(v):
            raise BusinessException(codigo=422, mensaje="La tarjeta no cumple las validaciones Luhn")

        return v
    
    @field_validator("cvv")
    def validar_cvv(cls, v):
        if not CVV_PATTERN.match(v):
            raise BusinessException(codigo=422, mensaje="El CVV no tiene un formato correcto")
        
        return v
    
    @field_validator("expiracion")
    def validar_expiracion(cls, v):
        matcher = EXPIRACION_PATTERN.match(v)
        if not matcher:
            raise BusinessException(codigo=422, mensaje="La fecha de expiracion no tiene un formato correcto")
        
        year = matcher.group(2)
        if int(year) < (datetime.now().year % 100):
            raise BusinessException(codigo=403, mensaje="No puede registrar una tarjeta vencida")

        return v
    
class CrearTarjetaResponse(BaseModel):
    id: str

class ConsultarTarjetaResponse(BaseModel):
    id: str
    cliente_id: str
    numero_tarjeta: str
    cvv: str
    expiracion: str
    activa: bool
    bin: str
    terminacion: str
    fecha_creacion: str
    fecha_actualizacion: Optional[str]

class ActualizarTarjetaRequest(BaseModel):
    cliente_id: str
    cvv: str
    activa: bool

    @field_validator("cvv")
    def validar_cvv(cls, v):
        if not CVV_PATTERN.match(v):
            raise BusinessException(codigo=422, mensaje="El CVV no tiene un formato correcto")
        
        return v

class ActualizarTarjetaResponse(BaseModel):
    actualizada: bool

class EliminarTarjetaResponse(BaseModel):
    eliminada: bool