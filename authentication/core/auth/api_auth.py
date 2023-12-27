from __future__ import annotations

from fastapi import APIRouter, Form

from core.auth.auth_services import AuthService
from core.pydantic_models import Token

from core.pydantic_models import UserSchemaCreate
from utils.dependencies import uow_dependency
from utils.dependencies import (
    user_by_credentials_dependency,
    user_by_token_dependency,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
def health() -> dict:
    return {"ping": "pong"}


@router.post("/login", response_model=Token)
async def log_in_for_access_token(
        user: user_by_credentials_dependency,
) -> Token:
    return await AuthService.login(user)


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
):
    user_data = UserSchemaCreate(username=username, password=password, email=email)
    return await AuthService.signup(user_data=user_data, uow=uow)
