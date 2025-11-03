from __future__ import annotations

import asyncio
from typing import Any, Callable

import httpx


DEFAULT_TIMEOUT = httpx.Timeout(connect=3.0, read=5.0, write=5.0, pool=5.0)


async def get_with_retries(
    url: str,
    *,
    client_factory: Callable[[], httpx.AsyncClient] | None = None,
    retries: int = 2,
    backoff_seconds: float = 0.2,
    timeout: httpx.Timeout = DEFAULT_TIMEOUT,
) -> httpx.Response:
    factory = client_factory or (lambda: httpx.AsyncClient(timeout=timeout, follow_redirects=True))
    attempt = 0
    last_exc: Exception | None = None
    while attempt <= retries:
        try:
            async with factory() as client:
                resp = await client.get(url)
                resp.raise_for_status()
                return resp
        except Exception as exc:  # noqa: BLE001 - deliberate boundary
            last_exc = exc
            if attempt == retries:
                raise
            await asyncio.sleep(backoff_seconds * (attempt + 1))
            attempt += 1
    # Should not happen
    assert last_exc is not None
    raise last_exc


