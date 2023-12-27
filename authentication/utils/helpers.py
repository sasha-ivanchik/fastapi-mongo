from jwt import InvalidTokenError
from fastapi import Form, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from core.connection import async_session_maker
from core.schemas import User
from utils.exceptions import SuperAuthException
from utils.hashing import Hasher
from utils.security import decode_jwt

http_bearer = HTTPBearer()


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


async def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    """get payload from token"""
    token = credentials.credentials
    try:
        payload = decode_jwt(token)
        return payload
    except InvalidTokenError:
        raise SuperAuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


async def get_user_by_token(
    token_payload: dict = Depends(get_token_payload),
) -> User:
    """get user by token"""
    invalid_token_error = SuperAuthException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )

    username: str | None = token_payload.get("username")
    if not username:
        raise invalid_token_error
    try:
        async with async_session_maker() as session:
            user = await session.execute(select(User).where(User.username == username))
            user = user.scalars().one()

            if not user:
                raise invalid_token_error

            return user

    except SQLAlchemyError as e:
        raise SuperAuthException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Problem with DB. Check data and Retry.\n{e}",
        )
