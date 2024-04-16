from __future__ import annotations

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import status

from core.pydantic_models import UserSchema, UserSchemaCreate, TokenInfo
from core.users.services import UsersService
from utils.exceptions import SuperAuthException
from utils.hashing import Hasher
from utils.unit_of_work import ProtocolUnitOfWork
from utils.helpers import create_access_token, create_refresh_token


class AuthService:
    """handles all necessary actions with passwords and tokens"""

    @staticmethod
    async def login(
            user: UserSchema,
            uow: ProtocolUnitOfWork,
    ) -> TokenInfo:
        access_token = create_access_token(user=user)
        refresh_token = create_refresh_token(user=user)

        await AuthService.put_refresh_in_db(
            uow=uow,
            some_user=user,
            refresh_token=refresh_token
        )

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @staticmethod
    async def signup(
            user_data: UserSchemaCreate,
            uow: ProtocolUnitOfWork,
    ) -> TokenInfo:
        new_user = await UsersService.create(uow, user_data)
        return await AuthService.login(user=new_user, uow=uow)

    @staticmethod
    async def put_refresh_in_db(
            uow: ProtocolUnitOfWork,
            some_user: UserSchema,
            refresh_token: str,
    ):
        """puts refresh token in db"""
        async with uow:
            new_token_dict = {"user_id": some_user.id}
            new_token_dict["hashed_token"] = Hasher.get_password_hash(
                refresh_token
            )
            try:
                token_count = await uow.token_repo.count_token_by_user_id(some_user.id)
                if not token_count:
                    new_token = await uow.token_repo.create(new_token_dict)
                else:
                    new_token = await uow.token_repo.update_hashed_token(
                        user_id=some_user.id,
                        new_hashed_token=new_token_dict["hashed_token"]
                    )
                await uow.commit()
                return new_token

            except IntegrityError as e:
                if "UniqueViolationError" in str(e):
                    raise SuperAuthException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"User with such data already exists.",
                    )

            except SQLAlchemyError as e:
                raise SuperAuthException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"auth service: {e}",
                )
