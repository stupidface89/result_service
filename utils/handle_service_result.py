import json

from fastapi.responses import JSONResponse
from fastapi import status

from ..schemas.api_response_schemas import ApiResponseSchema
from ..core import Result


def handle_service_result(service_result: Result) -> JSONResponse:
    """
    Return Fastapi JSONResponse from Result
    """
    if not hasattr(service_result, 'is_success'):
        raise ValueError('Не удалось распарсить Service Result сущность - нет аттрибута is_success.')

    if service_result.is_success:
        content = ApiResponseSchema(
            success=True,
            data=service_result.data
        ).json()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=json.loads(content)
        )

    else:
        http_status = service_result.status_code or status.HTTP_400_BAD_REQUEST
        content = ApiResponseSchema(
            success=False,
            data=None,
            error={
                "code": service_result.error.name,
                "message": service_result.error_message
            }
        ).json()

        return JSONResponse(
            status_code=http_status,
            content=json.loads(content)
        )