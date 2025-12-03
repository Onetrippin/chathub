from typing import Any
from starlette.requests import Request
from services.http_client import http_get, http_post, http_delete

def _with_request_id_headers(request: Request, headers: dict | None):
    merged = dict(headers or {})
    rid = getattr(request.state, "request_id", None)
    if rid:
        merged["X-Request-ID"] = rid
    return merged

async def ctx_get(request: Request, url: str, **kwargs) -> Any:
    kwargs["headers"] = _with_request_id_headers(request, kwargs.get("headers"))
    return await http_get(url, **kwargs)

async def ctx_post(request: Request, url: str, json: Any = None, **kwargs) -> Any:
    kwargs["headers"] = _with_request_id_headers(request, kwargs.get("headers"))
    return await http_post(url, json=json, **kwargs)

async def ctx_delete(request: Request, url: str, **kwargs) -> Any:
    kwargs["headers"] = _with_request_id_headers(request, kwargs.get("headers"))
    return await http_delete(url, **kwargs)
