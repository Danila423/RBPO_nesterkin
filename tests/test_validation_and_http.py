import httpx
import pytest

from app.core.http import DEFAULT_TIMEOUT, get_with_retries
from app.main import app


@pytest.mark.asyncio
async def test_price_validation_rejects_long_query():
    long_q = "x" * 51
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/price/", params={"query": long_q})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_price_validation_rejects_bad_chars():
    bad = "DROP TABLE;"
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/price/", params={"query": bad})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_http_client_retries_then_succeeds():
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] < 2:
            raise httpx.ReadTimeout("boom")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)

    async def client_factory():
        return httpx.AsyncClient(timeout=DEFAULT_TIMEOUT, transport=transport)

    resp = await get_with_retries(
        "http://example", client_factory=client_factory, retries=2
    )
    assert resp.status_code == 200 and calls["n"] == 2


@pytest.mark.asyncio
async def test_http_client_eventual_timeout():
    def handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timeout")

    transport = httpx.MockTransport(handler)

    async def client_factory():
        timeout = httpx.Timeout(0.01, read=0.01, connect=0.01)
        return httpx.AsyncClient(timeout=timeout, transport=transport)

    with pytest.raises(httpx.ReadTimeout):
        await get_with_retries(
            "http://example",
            client_factory=client_factory,
            retries=1,
            backoff_seconds=0,
        )
