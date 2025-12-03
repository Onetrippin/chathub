import asyncio
from typing import Any, Optional

from curl_cffi.requests import AsyncSession
from curl_cffi.requests.exceptions import HTTPError

from config import HTTP_IMPERSONATE, HTTP_TIMEOUT_SECONDS, HTTP_RETRIES

_session: Optional[AsyncSession] = None


async def init_http_client() -> None:
    global _session
    if _session is None:
        _session = AsyncSession(impersonate=HTTP_IMPERSONATE)


async def close_http_client() -> None:
    global _session
    if _session is not None:
        await _session.close()
        _session = None


def _get_session() -> AsyncSession:
    if _session is None:
        raise RuntimeError("HTTP client is not initialized. Call init_http_client() on startup.")
    return _session


async def _request_json(method: str, url: str, *, json: Any = None, **kwargs) -> Any:
    s = _get_session()
    timeout = kwargs.pop("timeout", HTTP_TIMEOUT_SECONDS)

    last_exc: Exception | None = None
    for attempt in range(HTTP_RETRIES + 1):
        try:
            r = await s.request(method, url, json=json, timeout=timeout, **kwargs)
            r.raise_for_status()  # curl_cffi raises HTTPError on non-2xx. [web:149]
            return r.json()
        except (HTTPError, OSError) as e:
            last_exc = e
            if attempt >= HTTP_RETRIES:
                raise
            await asyncio.sleep(0.2 * (attempt + 1))

    raise last_exc or RuntimeError("Unknown HTTP error")


async def http_get(url: str, **kwargs) -> Any:
    return await _request_json("GET", url, **kwargs)


async def http_post(url: str, json: Any = None, **kwargs) -> Any:
    return await _request_json("POST", url, json=json, **kwargs)


async def http_delete(url: str, **kwargs) -> Any:
    s = _get_session()
    r = await s.delete(url, timeout=HTTP_TIMEOUT_SECONDS, **kwargs)
    r.raise_for_status()
    return r.json() if getattr(r, "content", None) else None
