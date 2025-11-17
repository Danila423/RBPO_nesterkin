import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.main import app
from app.models.user import User
from app.models.wish import Wish


@pytest.mark.asyncio
async def test_create_and_get_wish() -> None:
    async with AsyncSessionLocal() as db:
        user = User(
            username="test_user",
            email="test_user@example.com",
            password_hash=hash_password("1234"),
            role="admin",
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        login = await ac.post(
            "/auth/login",
            data={"username": "test_user", "password": "1234"},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        assert login.status_code == 200
        tokens = login.json()
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}

        async with AsyncSessionLocal() as db:
            wish = Wish(
                user_id=user.id,
                title="Test PS5",
                link="https://store.playstation.com",
                price_estimate=499.99,
                notes="Want it badly!",
            )
            db.add(wish)
            await db.commit()
            await db.refresh(wish)

        response = await ac.get(f"/wishes/{wish.id}", headers=headers)
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Test PS5"
        assert float(body["price_estimate"]) == 499.99

    async with AsyncSessionLocal() as db:
        await db.execute(text("DELETE FROM wishes"))
        await db.execute(text("DELETE FROM users"))
        await db.commit()


@pytest.mark.asyncio
async def test_delete_wish() -> None:
    async with AsyncSessionLocal() as db:
        user = User(
            username="deleter",
            email="deleter@example.com",
            password_hash=hash_password("delete123"),
            role="admin",
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        login = await ac.post(
            "/auth/login",
            data={"username": "deleter", "password": "delete123"},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        assert login.status_code == 200
        tokens = login.json()
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}

        async with AsyncSessionLocal() as db:
            wish = Wish(
                user_id=user.id,
                title="Temporary Wish",
                link="https://example.com",
                price_estimate=100,
                notes="Temporary data",
            )
            db.add(wish)
            await db.commit()
            await db.refresh(wish)

        response = await ac.delete(f"/wishes/{wish.id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["status"] == "deleted"

        async with AsyncSessionLocal() as db:
            result = await db.execute(
                text("SELECT COUNT(*) FROM wishes WHERE id=:id"), {"id": wish.id}
            )
            count = result.scalar()
            assert count == 0
            await db.execute(text("DELETE FROM wishes"))
            await db.execute(text("DELETE FROM users"))
            await db.commit()
