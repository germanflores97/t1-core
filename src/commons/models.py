from bson import ObjectId
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(lambda v: str(v))
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return cls(v)
        if isinstance(v, str):
            try:
                return cls(ObjectId(v))
            except Exception:
                raise ValueError("Invalid ObjectId string")
        raise TypeError("ObjectId or valid ObjectId string required")