from fastapi import Header, HTTPException
from services.http_client import http_get
from services.errors import downstream_error
from config import AUTH_URL


async def verify_jwt(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Empty token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        result = await http_get(
            f"{AUTH_URL}/internal/verify",
            headers={"Authorization": f"Bearer {token}"},
        )
    except Exception as e:
        downstream_error(502, f"Auth verify failed: {type(e).__name__}", "auth-service")

    if not result.get("valid"):
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result["user_id"]
