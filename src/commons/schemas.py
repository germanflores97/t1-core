from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class GenericResponse(BaseModel, Generic[T]):
    mensaje: str
    respuesta: Optional[T] = None