from __future__ import annotations

from fastapi import APIRouter, Form, status
from starlette.responses import JSONResponse
from pydantic import ValidationError

from core.auth.auth_services import AuthService
from core.users.services import UsersService
from core.pydantic_models import (
    AuthResponse,
    ResponseStatus,
    UserBase,
)

from core.pydantic_models import UserSchemaCreate
from utils.dependencies import uow_dependency
from utils.dependencies import (
    user_by_token_dependency,
    user_by_refresh_token_dependency,
)
from utils.exceptions import SuperAuthException
from utils.prep_response import prep_api_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
def health() -> dict:
    return {"ping": "pong"}


@router.post("/login", response_model=AuthResponse)
async def log_in_for_access_token(
        uow: uow_dependency,
        username: str = Form(),
        password: str = Form(),
) -> JSONResponse:

    user = await UsersService.get_user_by_creds(
        uow=uow,
        username=username,
        password=password
    )
    result = await AuthService.login(uow=uow, user=user)
    return prep_api_response(
        status=ResponseStatus.success.value,
        message="Client has successfully logged in.",
        data=result,
    )


@router.get("/me", response_model=AuthResponse)
async def get_self_info(
        user: user_by_token_dependency,
) -> JSONResponse:
    return prep_api_response(
        status=ResponseStatus.success.value,
        message="Client information provided.",
        data=UserBase(
            username=user.username,
            email=user.email,
            role=user.role
        ),
    )


@router.post("/signup", response_model=AuthResponse)
async def sign_up_for_access_token(
        uow: uow_dependency,
        username: str = Form(),
        password: str = Form(),
        email: str = Form(),
) -> JSONResponse:
    try:
        user_data = UserSchemaCreate(username=username, password=password, email=email)
    except ValidationError:
        raise SuperAuthException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error. Probably, username is too short (min 3 symbols).",
        )
    result = await AuthService.signup(user_data=user_data, uow=uow)
    return prep_api_response(
        status=ResponseStatus.success.value,
        message="Client has been successfully registered.",
        data=result,
    )


@router.post("/refresh", response_model=AuthResponse)
async def auth_refresh_jwt(
        uow: uow_dependency,
        user: user_by_refresh_token_dependency,
) -> JSONResponse:
    result = await AuthService.login(uow=uow, user=user)
    return prep_api_response(
        status=ResponseStatus.success.value,
        message="Access data has been successfully updated.",
        data=result,
    )
