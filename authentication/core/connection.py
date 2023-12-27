from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

engine = create_async_engine(
    settings.AUTH_DATABASE_URL,
    future=True,
    echo=True,
)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator:
    """returns async session"""
    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()
