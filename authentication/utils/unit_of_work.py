from abc import ABC, abstractmethod

from core.connection import async_session_maker
from utils.repositories import UsersRepository


class ProtocolUnitOfWork(ABC):
    users_repo: UsersRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(ProtocolUnitOfWork):
    def __init__(self):
        super().__init__()
        self.session_maker = async_session_maker

    async def __aenter__(self):
        self.session = self.session_maker()
        self.users_repo = UsersRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
