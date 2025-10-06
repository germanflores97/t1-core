from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from src.commons.models import PyObjectId

class Cobro(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    tarjeta_id: PyObjectId
    importe: float
    fecha_operacion: datetime
    concepto: Optional[str]
    estatus: bool
    descripcion_estatus: str
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    reembolsado: bool
    fecha_reembolso: Optional[datetime] = None

    def to_mongo(self) -> dict:
        doc = self.model_dump(by_alias=True)
        objectid_fields = ["_id", "tarjeta_id"]

        for field in objectid_fields:
            if field in doc and isinstance(doc[field], str) and ObjectId.is_valid(doc[field]):
                doc[field] = ObjectId(doc[field])

        return doc

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
