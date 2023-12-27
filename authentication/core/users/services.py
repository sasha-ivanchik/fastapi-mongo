from __future__ import annotations

from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from starlette import status

from core.pydantic_models import UserSchema, UserSchemaCreate, UserSchemaUpdate
from utils.exceptions import SuperAuthException
from utils.hashing import Hasher
from utils.unit_of_work import ProtocolUnitOfWork


class UsersService:
    """handles all necessary actions with user"""

    @staticmethod
    async def create(
        uow: ProtocolUnitOfWork,
        some_user: UserSchemaCreate,
    ) -> UserSchema:
        """creates new user"""
        async with uow:
            try:
                new_user_dict = some_user.model_dump()
                del new_user_dict["password"]

                new_user_dict["hashed_password"] = Hasher.get_password_hash(
                    some_user.password
                )

                new_user = await uow.users_repo.create(new_user_dict)
                await uow.commit()
                return new_user

            except IntegrityError as e:
                if "UniqueViolationError" in str(e):
                    raise SuperAuthException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"User with such data already exists.",
                    )
            except SQLAlchemyError:
                raise SuperAuthException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Problem with creating user. Check data and Retry.",
                )

    @staticmethod
    async def get_list(uow: ProtocolUnitOfWork) -> list[UserSchema]:
        """reads all users"""
        async with uow:
            try:
                return await uow.users_repo.get_list()
            except SQLAlchemyError:
                raise SuperAuthException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Problem with getting users. Check data and Retry.",
                )

    @staticmethod
    async def get(uow: ProtocolUnitOfWork, user_id: int) -> UserSchema:
        """gets user by id"""
        async with uow:
            try:
                return await uow.users_repo.get(user_id)

            except NoResultFound:
                raise SuperAuthException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Not found.",
                )
            except SQLAlchemyError:
                raise SuperAuthException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Problem with getting user. Check data and Retry.",
                )

    @staticmethod
    async def delete(uow: ProtocolUnitOfWork, user_id: int) -> None:
        """deletes user by id"""
        async with uow:
            try:
                await uow.users_repo.delete(user_id)
                await uow.commit()

            except NoResultFound:
                raise SuperAuthException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Not found.",
                )
            except SQLAlchemyError:
                raise SuperAuthException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Problem with deleting the user. Check data and Retry.",
                )

    @staticmethod
    async def update(
        uow: ProtocolUnitOfWork,
        incoming_user_id: int,
        incoming_user_data: UserSchemaUpdate,
    ) -> UserSchema:
        """updates user by id"""
        async with uow:
            try:
                updated_user = await uow.users_repo.update(
                    incoming_user_id, incoming_user_data
                )
                await uow.commit()
                return updated_user

            except NoResultFound:
                raise SuperAuthException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Not found.",
                )
            except SQLAlchemyError:
                raise SuperAuthException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Problem with updating the user. Check data and Retry.",
                )
