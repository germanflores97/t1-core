from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

from src.commons.models import PyObjectId

class Cliente(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    curp: str
    email: str
    telefono: str
    activo: bool
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    def to_mongo(self) -> dict:
        doc = self.model_dump(by_alias=True)

        if "_id" in doc and isinstance(doc["_id"], str):
            try:
                doc["_id"] = ObjectId(doc["_id"])
            except:
                pass

        return doc

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True