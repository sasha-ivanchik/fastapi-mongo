from __future__ import annotations

from fastapi import APIRouter, Form, status
from pydantic import ValidationError

from core.auth.auth_services import AuthService
from core.pydantic_models import TokenInfo

from core.pydantic_models import UserSchemaCreate
from utils.dependencies import uow_dependency
from utils.dependencies import (
    user_by_credentials_dependency,
    user_by_token_dependency,
    user_by_refresh_token_dependency,
)
from utils.exceptions import SuperAuthException

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
def health() -> dict:
    return {"ping": "pong"}


@router.post("/login", response_model=TokenInfo)
async def log_in_for_access_token(
        uow: uow_dependency,
        user: user_by_credentials_dependency,
) -> TokenInfo:
    return await AuthService.login(uow=uow, user=user)


@router.get("/me")
async def get_self_info(
        user: user_by_token_dependency,
) -> dict:
    return {
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }


@router.post("/signup")
async def sign_up_for_access_token(
        uow: uow_dependency,
        username: str = Form(),
        password: str = Form(),
        email: str = Form(),
) -> TokenInfo:
    try:
        user_data = UserSchemaCreate(username=username, password=password, email=email)
    except ValidationError:
        raise SuperAuthException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error. Probably, username is too short (min 3 symbols).",
        )
    return await AuthService.signup(user_data=user_data, uow=uow)


@router.post("/refresh")
async def auth_refresh_jwt(
        uow: uow_dependency,
        user: user_by_refresh_token_dependency,
) -> TokenInfo:
    return await AuthService.login(uow=uow, user=user)
