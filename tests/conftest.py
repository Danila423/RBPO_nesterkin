# tests/conftest.py
# isort: skip_file
# ruff: noqa: E402,I001
import os
import sys
from pathlib import Path
from typing import AsyncIterator

from fastapi import Depends
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.database import (
    AsyncSession,
    AsyncSessionLocal,
    Base,
    engine,
    get_db,
)  # noqa: E402
from app.core.deps import get_current_user  # noqa: E402
from app.models.user import User  # noqa: E402
from app.main import app  # noqa: E402


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _init_db() -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture()
async def client(db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    async def override_get_current_user(
        db: AsyncSession = Depends(get_db),
    ) -> User:
        result = await db.execute(select(User).order_by(User.id))
        user = result.scalars().first()
        if not user:
            user = User(
                username="testadmin",
                email="testadmin@example.com",
                password_hash="test",
                role="admin",
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
