from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette import status as status_code
from starlette.responses import JSONResponse

from core.models import ResponseStatus
from utils.exceptions import SuperApiException
from utils.response_prep import prep_api_response


def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> JSONResponse:
    """422 error handler"""
    return prep_api_response(
        response_status=ResponseStatus.error,
        code=status_code.HTTP_422_UNPROCESSABLE_ENTITY,
        message=f"{request.url.path} => Unprocessable entity. Check your data and retry.",
        response_data=None,
        user=None,
    )


def http_exception_handler(request: Request, exc: SuperApiException) -> JSONResponse:
    """main error handler"""
    return prep_api_response(
        response_status=ResponseStatus.error.value,
        code=int(exc.status_code),
        message=f"{request.url.path} => {exc.detail}",
        response_data=None,
        user=None,
    )


def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    incoming_status_code = (
        int(exc.code) if hasattr(exc, "code") else status_code.HTTP_500_INTERNAL_SERVER_ERROR
    )
    return prep_api_response(
        response_status=ResponseStatus.error.value,
        code=incoming_status_code,
        message=f"{request.url.path} => {type(exc).__name__} : {exc}",
        response_data=None,
        user=None,
    )


def method_not_allowed_handler(request: Request, exc: Exception) -> JSONResponse:
    """405 error handler"""
    return prep_api_response(
        response_status=ResponseStatus.error.value,
        code=status_code.HTTP_405_METHOD_NOT_ALLOWED,
        message=f"{request.url.path} => {exc}. Check your request",
        response_data=None,
        user=None,
    )


def not_found_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """404 error handler"""
    return prep_api_response(
        response_status=ResponseStatus.error.value,
        code=status_code.HTTP_404_NOT_FOUND,
        message=f"{request.url.path} => There is no data. Check your request",
        response_data=None,
        user=None
    )


registered_exception_handlers = {
    RequestValidationError: request_validation_exception_handler,
    SuperApiException: http_exception_handler,
    405: method_not_allowed_handler,
    404: not_found_exception_handler,
    Exception: unhandled_exception_handler,
}
