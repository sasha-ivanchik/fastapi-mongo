from jwt import InvalidTokenError, ExpiredSignatureError
from fastapi import (
    Form,
    Depends,
    Header,
)

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from core.users.services import UsersService
from core.connection import async_session_maker
from core.pydantic_models import UserSchema, Role
from core.schemas import User
from utils.exceptions import SuperAuthException
from utils.hashing import Hasher
from utils.security import decode_jwt, encode_jwt
from utils.constants import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE
)
from config import settings
from utils.unit_of_work import UnitOfWork, ProtocolUnitOfWork


async def get_user_by_credentials(
        username: str = Form(),
        password: str = Form(),
) -> User:
    """get user by username and password"""
    unauthenticated_error = SuperAuthException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    try:
        async with async_session_maker() as session:
            user = await session.execute(select(User).where(User.username == username))
            user = user.scalars().one()

            if not user:
                raise unauthenticated_error
            if not Hasher.verify_password(password, user.hashed_password):
                raise unauthenticated_error

            return user

    except SQLAlchemyError as e:
        raise SuperAuthException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Problem with DB. Check data and Retry.\n{e}",
        )


async def fetch_token_data(token_header: str) -> dict:
    """handle fetching data from token payload"""
    if token_header is None:
        raise SuperAuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token needed",
        )
    try:
        payload = decode_jwt(token_header)
        return payload
    except ExpiredSignatureError:
        raise SuperAuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token expired. Go to 'LOG IN'",
        )
    except InvalidTokenError:
        raise SuperAuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token",
        )


async def get_access_token_payload(
        auth: str | None = Header(None),
) -> dict:
    """get payload from access token"""
    return await fetch_token_data(auth)


async def get_refresh_token_payload(
        refresh: str | None = Header(None),
) -> dict:
    """get payload from refresh token"""
    return await fetch_token_data(refresh)


def check_token_type(token_payload: dict, expected_token_type: str) -> None:
    """checks token type"""
    token_type: str | None = token_payload.get(TOKEN_TYPE_FIELD)
    if token_type != expected_token_type:
        raise SuperAuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type {token_type!r} expected {expected_token_type!r}",
        )


async def fetch_user_by_token(
        token_payload: dict,
        token_type: str,
        sub_field: str,
        uow: ProtocolUnitOfWork,
) -> UserSchema:
    check_token_type(
        token_payload=token_payload,
        expected_token_type=token_type
    )

    username: str | None = token_payload.get(sub_field)
    if not username:
        raise SuperAuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token (user not found)",
        )
    return await UsersService.get_user_by_username(uow, username)


async def get_user_by_access_token(
        token_payload: dict = Depends(get_access_token_payload),
        uow: ProtocolUnitOfWork = Depends(UnitOfWork),
) -> UserSchema:
    """get user by access token"""
    return await fetch_user_by_token(
        uow=uow,
        sub_field="username",
        token_payload=token_payload,
        token_type=ACCESS_TOKEN_TYPE,
    )


async def get_user_by_refresh_token(
        token_payload: dict = Depends(get_refresh_token_payload),
        uow: ProtocolUnitOfWork = Depends(UnitOfWork),
) -> UserSchema:
    """get user by refresh token"""
    return await fetch_user_by_token(
        uow=uow,
        sub_field="sub",
        token_payload=token_payload,
        token_type=REFRESH_TOKEN_TYPE,
    )


def create_jwt(
        token_type: str,
        token_payload: dict,
        expire_timedelta_sec: int | None = settings.AUTH_JWT.ACCESS_TOKEN_EXPIRE_SEC,
        expire_timedelta_days: int | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_payload)
    return encode_jwt(
        payload=jwt_payload,
        expire_timedelta_sec=expire_timedelta_sec,
        expire_timedelta_days=expire_timedelta_days,
    )


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        "username": user.username,
        "email": user.email,
        "role": user.role.value if isinstance(user.role, Role) else user.role,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_payload=jwt_payload,
        expire_timedelta_sec=settings.AUTH_JWT.ACCESS_TOKEN_EXPIRE_SEC,
    )


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.username,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_payload=jwt_payload,
        expire_timedelta_days=settings.AUTH_JWT.REFRESH_TOKEN_EXPIRE_DAYS,
    )
