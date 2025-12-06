import uuid
import jwt
from datetime import datetime, timedelta, timezone


def make_access_token(user_id: str, private_key_pem: str, issuer: str, ttl_seconds: int) -> tuple[str, int]:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(seconds=ttl_seconds)

    payload = {
        "sub": user_id,
        "iss": issuer,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
        "type": "access",
    }
    token = jwt.encode(payload, private_key_pem, algorithm="RS256")
    return token, ttl_seconds


def make_refresh_token(user_id: str, private_key_pem: str, issuer: str, ttl_seconds: int) -> tuple[str, int]:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(seconds=ttl_seconds)

    payload = {
        "sub": user_id,
        "iss": issuer,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
        "type": "refresh",
    }
    token = jwt.encode(payload, private_key_pem, algorithm="RS256")
    return token, ttl_seconds


def verify_jwt_token(token: str, public_key_pem: str, issuer: str, required_type: str = "access") -> str | None:
    try:
        payload = jwt.decode(
            token,
            public_key_pem,
            algorithms=["RS256"],
            options={"require": ["exp", "iat", "sub"]},
            issuer=issuer,
        )
        if payload.get("type") != required_type:
            return None
        return payload.get("sub")
    except Exception:
        return None
