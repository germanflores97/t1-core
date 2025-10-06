from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Cliente(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    curp: str
    email: str
    telefono: str
    activo: bool
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
