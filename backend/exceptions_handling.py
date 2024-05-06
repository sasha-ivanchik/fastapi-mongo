from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from app.utils.response_utils import error_json_response


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """422 error handler"""
    return await error_json_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        exc_type=type(exc).__name__,
        exc=f"422 => {request.url.path} => {exc}",
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """main error handler"""
    return await error_json_response(
        status_code=exc.status_code,
        exc_type=type(exc).__name__,
        exc=f"{exc.status_code} => {request.url.path} => {exc.detail}",
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    status_code = (
        int(exc.code) if hasattr(exc, "code") else status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    return await error_json_response(
        status_code=status_code,
        exc_type=type(exc).__name__,
        exc=f"{status_code} => {request.url.path} => {exc}",
    )


async def method_not_allowed_handler(request: Request, exc: Exception):
    """405 error handler"""
    return await error_json_response(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        exc_type="Method not allowed",
        exc=f"405 => {request.url.path} => Method not allowed. {exc}",
    )


async def not_found_exception_handler(request: Request, exc: Exception):
    """404 error handler"""
    return await error_json_response(
        status_code=status.HTTP_404_NOT_FOUND,
        exc_type="Not found error",
        exc=f"404 => {request.url.path} => URL is not correct. {exc}",
    )


registered_exception_handlers = {
    RequestValidationError: request_validation_exception_handler,
    HTTPException: http_exception_handler,
    405: method_not_allowed_handler,
    404: not_found_exception_handler,
}
