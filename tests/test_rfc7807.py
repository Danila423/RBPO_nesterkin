import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_not_found_problem_details_has_correlation_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/this-path-does-not-exist")
    assert r.status_code == 404
    body = r.json()
    assert set(["type", "title", "status", "detail", "correlation_id"]).issubset(
        body.keys()
    )
    assert isinstance(body["correlation_id"], str) and len(body["correlation_id"]) > 0


@pytest.mark.asyncio
async def test_validation_error_is_rfc7807():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/price/")
    assert r.status_code == 422
    body = r.json()
    assert body["title"] == "Validation Error"
    assert body["status"] == 422
    assert "errors" in body
    assert "correlation_id" in body
