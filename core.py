from typing import TypeVar, Generic, Union
from enum import Enum
from dataclasses import dataclass


class ServiceError(Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    BUSINESS_RULE_VIOLATION = "BUSINESS_RULE_VIOLATION"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    FORBIDDEN = "FORBIDDEN"
    THIRD_PARTY_AUTHENTICATION_ERROR = "THIRD_PARTY_AUTHENTICATION_ERROR"
    THIRD_PARTY_ERROR = "THIRD_PARTY_ERROR"


error_status_codes = {
    ServiceError.VALIDATION_ERROR: 422,
    ServiceError.NOT_FOUND: 404,
    ServiceError.ALREADY_EXISTS: 400,
    ServiceError.BUSINESS_RULE_VIOLATION: 400,
    ServiceError.BAD_REQUEST: 400,
    ServiceError.SERVICE_UNAVAILABLE: 503,
    ServiceError.AUTHENTICATION_ERROR: 401,
    ServiceError.FORBIDDEN: 403,
    ServiceError.THIRD_PARTY_AUTHENTICATION_ERROR: 503,
    ServiceError.THIRD_PARTY_ERROR: 504
}

T = TypeVar('T')
E = TypeVar('E', bound=ServiceError)


@dataclass
class Result(Generic[T, E]):
    is_success: bool
    data: Union[T, None] = None
    error: Union[E, None] = None
    status_code: Union[int, None] = None
    error_message: Union[str, None] = None

    @classmethod
    def success(cls, data: T) -> 'Result[T, E]':
        return cls(is_success=True, data=data)

    @classmethod
    def fail(cls, error: E, error_message: str) -> 'Result[T, E]':
        return cls(
            is_success=False,
            error=error,
            status_code=error_status_codes[error],
            error_message=error_message
        )

    @classmethod
    def return_error(cls):
        if cls.error is None and cls.error_message is None:
            raise ValueError(f'Could not return error from {cls.__name__} '
                             'instance, most likely Result was likely not an error.')

        return cls
