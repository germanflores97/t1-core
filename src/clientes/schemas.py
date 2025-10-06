from pydantic import Field, field_validator, BaseModel
from fastapi.exceptions import HTTPException
import re
from typing import Optional

CURP_PATTERN = re.compile( #Se compila el pattern de validacion para un mejor performance
    r"^[A-Z][AEIOU][A-Z]{2}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[HM]"\
    r"(AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)"\
    r"[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]\d$"
)

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$") #Se compila el pattern de validacion para un mejor performance

class CrearClienteRequest(BaseModel):
    """
        <p>Clase utilizada como request para crear un cliente.</p>
    """
    nombres: str = Field(min_length=5, max_length=50)
    apellido_paterno: str = Field(min_length=5, max_length=40)
    apellido_materno: str = Field(min_length=5, max_length=40)
    curp: str = Field(min_length=18, max_length=18)
    email: str = Field(min_length=5, max_length=80)
    telefono: str = Field(min_length=12, max_length=12)

    @field_validator("curp")
    def validar_curp(cls, v):
        if not CURP_PATTERN.match(v.upper()):
            raise HTTPException(422, "El CURP no tiene un formato valido")
        
        return v.upper()
    
    @field_validator("email")
    def validar_email(cls, v):
        if not EMAIL_PATTERN.match(v):
            raise HTTPException(422, "Estructura del email no valida")
        
        return v

class CrearClienteResponse(BaseModel):
    id: str

class ActualizarClienteRequest(CrearClienteRequest):
    """
        <p>Clase utilizada como request para actualizar un cliente.</p>
    """
    activo: bool

class ActualizarClienteResponse(BaseModel):
    actualizado: bool

class ConsultarClienteResponse(BaseModel):
    id: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    curp: str
    email: str
    telefono: str
    activo: bool
    fecha_creacion: str
    fecha_actualizacion: Optional[str]

class EliminarClienteResponse(BaseModel):
    eliminado: bool