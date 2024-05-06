from typing import Union

from fastapi import status as status_code
from starlette.responses import JSONResponse

from core.pydantic_models import AuthResponse, ResponseStatus, TokenInfo, UserBase


def prep_api_response(
        status: ResponseStatus,
        message: str,
        data: Union[TokenInfo | UserBase | None],
        error: str | None = None,
        code: int = status_code.HTTP_200_OK,
) -> JSONResponse:
    api_response = AuthResponse(
        status=status,
        code=code,
        message=message,
        data=data,
        error=error
    )
    return JSONResponse(content=api_response.model_dump())
