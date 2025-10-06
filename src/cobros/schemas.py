from pydantic import BaseModel, Field, field_validator
from fastapi.exceptions import HTTPException
from typing import Optional
from datetime import datetime
import re

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
            raise HTTPException(422, "La fecha no tiene un formato de \"YYYY/MM/DD HH24:MI:SS\"")
        
        return v
    
    @field_validator("cvv")
    def validar_cvv(cls, v):
        if not CVV_PATTERN.match(v):
            raise HTTPException(422, "El CVV no tiene un formato correcto")
        
        return v

class AplicarCobroResponse(BaseModel):
    aplicado: bool
    detalle: str