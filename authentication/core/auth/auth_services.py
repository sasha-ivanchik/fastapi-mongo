from __future__ import annotations

from datetime import timedelta

from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from starlette import status

from core.pydantic_models import UserSchema, UserSchemaCreate, UserSchemaUpdate, Token

from core.users.services import UsersService
from utils.exceptions import SuperAuthException
from utils.hashing import Hasher
from utils.security import encode_jwt
from utils.unit_of_work import ProtocolUnitOfWork
from config import settings


class AuthService:
    """handles all necessary actions with passwords and tokens"""

    @staticmethod
    async def login(
        user: UserSchema,
    ) -> Token:
        access_token = encode_jwt(
            payload={
                "username": user.username,
                "email": user.email,
            },
        )
        return Token(
            access_token=access_token,
            token_type="Bearer",
        )

    @staticmethod
    async def signup(
        user_data: UserSchemaCreate,
        uow: ProtocolUnitOfWork,
    ) -> Token:
        new_user = await UsersService.create(uow, user_data)
        return await AuthService.login(new_user)
