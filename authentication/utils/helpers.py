from jwt import InvalidTokenError, ExpiredSignatureError
from fastapi import (
    Depends,
    Header,
)

from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from core.users.services import UsersService
from core.pydantic_models import UserSchema
from utils.exceptions import SuperAuthException
from utils.hashing import Hasher
from utils.security import decode_jwt
from utils.constants import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE
)
from utils.unit_of_work import UnitOfWork, ProtocolUnitOfWork


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
            detail=f"Token expired. Go to 'LOG IN' or refresh",
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
        refresh: str | None,
) -> dict:
    """get payload from refresh token"""
    return await fetch_token_data(refresh)


def check_token_type(token_payload: dict, expected_token_type: str) -> None:
    """checks token type"""
    token_type: str | None = token_payload.get(TOKEN_TYPE_FIELD)
    if token_type != expected_token_type:
        raise SuperAuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type.",
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


async def validate_refresh_jwt(
        uow: ProtocolUnitOfWork,
        refresh_token: str,
        user_from_token: UserSchema,
):
    validate_exception = SuperAuthException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token (user not found)",
    )
    try:
        token_in_db = await uow.token_repo.get_token_by_user_id(
            user_id=user_from_token.id,
        )

        if Hasher.decrypt(token_in_db.hashed_token) != refresh_token:
            raise SuperAuthException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token.",
            )
    except SQLAlchemyError:
        raise validate_exception


async def get_user_by_refresh_token(
        refresh_token: str | None = Header(None),
        uow: ProtocolUnitOfWork = Depends(UnitOfWork),
) -> UserSchema:
    """get user by refresh token"""
    token_payload = await get_refresh_token_payload(refresh=refresh_token)

    user_from_token = await fetch_user_by_token(
        uow=uow,
        sub_field="sub",
        token_payload=token_payload,
        token_type=REFRESH_TOKEN_TYPE,
    )

    await validate_refresh_jwt(
        uow=uow,
        refresh_token=refresh_token,
        user_from_token=user_from_token
    )

    return user_from_token
