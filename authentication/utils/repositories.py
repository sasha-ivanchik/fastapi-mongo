from abc import ABC, abstractmethod

from fastapi import status
from pydantic import BaseModel
from sqlalchemy import literal_column, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.pydantic_models import UserSchemaUpdate
from core.schemas import User, Token
from utils.exceptions import SuperAuthException
from utils.hashing import Hasher
from sqlalchemy.exc import SQLAlchemyError, NoResultFound


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, some_data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_list(self):
        raise NotImplementedError

    @abstractmethod
    async def _get(self, some_id):
        raise NotImplementedError

    @abstractmethod
    async def get(self, some_id):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, some_id):
        raise NotImplementedError

    @abstractmethod
    async def update(self, some_id, some_data):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, some_data: dict):
        statement = (
            insert(self.model).values(**some_data).returning(literal_column("*"))
        )
        result = await self.session.execute(statement)
        return result.one()

    async def get_list(self):
        statement = select(self.model)
        res = await self.session.execute(statement)
        return res.scalars().all()

    async def _get(self, some_id: int):
        res = await self.session.execute(
            select(self.model).where(self.model.id == some_id),
        )
        return res.scalars().one()

    async def get(self, some_id: int):
        return await self._get(some_id)

    async def delete(self, some_id: int):
        delete_item = await self._get(some_id)
        await self.session.delete(delete_item)

    async def update(
            self,
            some_id: int,
            some_data: BaseModel,
    ):
        update_item = await self._get(some_id)
        for field, value in some_data:
            if value:
                setattr(update_item, field, value)

        self.session.add(update_item)
        return update_item


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def update(
            self,
            some_id: int,
            some_data: UserSchemaUpdate,
    ):
        update_item = await self._get(some_id)
        for field, value in some_data:
            if value:
                setattr(update_item, field, value)

        self.session.add(update_item)
        return update_item

    async def get_user_by_username(self, username: str):
        res = await self.session.execute(
            select(self.model).where(self.model.username == username),
        )
        return res.scalars().one()

    async def get_user_by_creds(self, username: str, password: str):
        """get user by username and password"""
        unauthenticated_error = SuperAuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
        try:
            user = await self.session.execute(select(User).where(User.username == username))
            user = user.scalars().one()

            if not user or not Hasher.verify_password(password, user.hashed_password):
                raise unauthenticated_error
            return user

        except NoResultFound:
            raise unauthenticated_error

        except SQLAlchemyError:
            raise SuperAuthException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bad request. Check your data and Retry.",
            )


class TokenRepository(SQLAlchemyRepository):
    model = Token

    async def delete_token_by_user_id(self, user_id: int):
        token_res = await self.session.execute(
            select(self.model).where(self.model.user_id == user_id),
        )
        token = token_res.scalars().one()
        await self.session.delete(token)

    async def get_token_by_user_id(self, user_id: int):
        token_res = await self.session.execute(
            select(self.model).where(self.model.user_id == user_id),
        )
        return token_res.scalars().one()

    async def count_token_by_user_id(self, user_id: int):
        count = await self.session.execute(
            select(
                func.count("*").filter(self.model.user_id == user_id)
            ),
        )
        return count.scalars().one()

    async def update_hashed_token(
            self,
            user_id: int,
            new_hashed_token: str,
    ):
        update_item = await self.get_token_by_user_id(user_id)
        setattr(update_item, "hashed_token", new_hashed_token)

        self.session.add(update_item)
        return update_item

    async def get_token_by_hash(self, incoming_hashed_token: str):
        ...
