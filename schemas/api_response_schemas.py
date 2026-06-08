from typing import TypeVar, Any, Generic

from pydantic import BaseModel, ConfigDict, Field, UUID4, field_serializer

from ..core import ServiceError
from schemas.base_schema import ResponseBaseSchema, BaseSchema

T = TypeVar('T', bound=ResponseBaseSchema)
E = TypeVar('E', bound=ServiceError)


class ErrorResponseSchema(BaseModel):
    """Схема для ошибок"""
    code: ServiceError = Field(description="Код ошибки")
    message: str | None = Field(defaul=None, description="Сообщение об ошибке")
    system_message: str | None = Field(default=None)

    @field_serializer('code')
    def serialize_error_code(self, code: ServiceError) -> str:
        if code is not None:
            return code.name


class ApiResponseSchema(BaseSchema, Generic[T]):
    success: bool
    error: ErrorResponseSchema | None = None
    data: Any | None = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={
            UUID4: str,
        }
    )

