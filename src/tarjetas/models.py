from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from src.commons.models import PyObjectId

class Tarjeta(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    cliente_id: PyObjectId
    numero_tarjeta: str
    cvv: str
    expiracion: str
    activa: bool
    bin: str
    terminacion: str
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    def to_mongo(self) -> dict:
        doc = self.model_dump(by_alias=True)
        objectid_fields = ["_id", "cliente_id"]

        for field in objectid_fields:
            if field in doc and isinstance(doc[field], str) and ObjectId.is_valid(doc[field]):
                doc[field] = ObjectId(doc[field])

        return doc

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
