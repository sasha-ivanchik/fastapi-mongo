from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette import status as status_code
from starlette.responses import JSONResponse

from core.pydantic_models import ResponseStatus
from utils.prep_response import prep_api_response
from utils.exceptions import SuperAuthException


def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> JSONResponse:
    """422 error handler"""
    return prep_api_response(
        status=ResponseStatus.error.value,
        code=status_code.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Validation problem with your data. Check your data and retry.",
        data=None,
        error=f"{request.url.path} => Unprocessable entity. Check your data and retry.",
    )


def http_exception_handler(request: Request, exc: SuperAuthException) -> JSONResponse:
    """main error handler"""
    return prep_api_response(
        status=ResponseStatus.error.value,
        code=int(exc.status_code),
        message=f"Problem occured. {exc.detail}",
        data=None,
        error=f"{request.url.path} => {exc.detail}",
    )


def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    incoming_status_code = (
        int(exc.code) if hasattr(exc, "code") else status_code.HTTP_500_INTERNAL_SERVER_ERROR
    )
    return prep_api_response(
        status=ResponseStatus.error.value,
        code=incoming_status_code,
        message="Problem occured.",
        data=None,
        error=f"{request.url.path} => {type(exc).__name__} : {exc}",
    )


def method_not_allowed_handler(request: Request, exc: Exception) -> JSONResponse:
    """405 error handler"""
    return prep_api_response(
        status=ResponseStatus.error.value,
        code=status_code.HTTP_405_METHOD_NOT_ALLOWED,
        message="Method not allowed.",
        data=None,
        error=f"{request.url.path} => {exc}. Check your request",
    )


def not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """404 error handler"""
    return prep_api_response(
        status=ResponseStatus.error.value,
        code=status_code.HTTP_404_NOT_FOUND,
        message="No data.",
        data=None,
        error=f"{request.url.path} => There is no data. Check your request",
    )


registered_exception_handlers = {
    RequestValidationError: request_validation_exception_handler,
    SuperAuthException: http_exception_handler,
    405: method_not_allowed_handler,
    404: not_found_exception_handler,
    Exception: unhandled_exception_handler,
}
