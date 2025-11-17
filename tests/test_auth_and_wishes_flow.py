import pytest
from httpx import AsyncClient

from app.core.security import decode_token


@pytest.mark.asyncio
async def test_register_login_and_refresh(client: AsyncClient) -> None:
    # register
    reg = await client.post(
        "/auth/register",
        json={"username": "u1", "email": "u1@example.com", "password": "pass1234"},
    )
    assert reg.status_code == 200

    # login
    login = await client.post(
        "/auth/login",
        data={"username": "u1", "password": "pass1234"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200
    tokens = login.json()
    assert "access_token" in tokens and "refresh_token" in tokens

    # refresh
    refresh = await client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert refresh.status_code == 200
    refreshed = refresh.json()
    payload = decode_token(refreshed["access_token"])
    assert payload and payload.get("sub") is not None


@pytest.mark.asyncio
async def test_wishes_crud(client: AsyncClient) -> None:
    login = await client.post(
        "/auth/register",
        json={
            "username": "wish_user",
            "email": "wish@example.com",
            "password": "pass1234",
        },
    )
    assert login.status_code == 200

    login = await client.post(
        "/auth/login",
        data={"username": "wish_user", "password": "pass1234"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    tokens = login.json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    # create wish
    create = await client.post(
        "/wishes/",
        json={
            "title": "Item",
            "link": "https://example.com",
            "price_estimate": 10.5,
            "notes": "note",
        },
        headers=headers,
    )
    assert create.status_code == 200
    wish_id = create.json()["id"]

    # list wishes
    list_resp = await client.get("/wishes/", headers=headers)
    assert list_resp.status_code == 200
    assert any(w["id"] == wish_id for w in list_resp.json())

    # delete wish
    delete_resp = await client.delete(f"/wishes/{wish_id}", headers=headers)
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"status": "deleted"}
