from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(str(settings.DATABASE_URL), future=True, echo=False)


class Base(DeclarativeBase):
    pass


AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


__all__ = ["AsyncSession", "AsyncSessionLocal", "Base", "engine", "get_db"]
