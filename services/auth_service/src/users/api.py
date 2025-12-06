import json
from datetime import datetime, timezone, timedelta

from django.conf import settings
from django.utils import timezone as dj_tz
from django.db import transaction
from ninja import NinjaAPI, Router
from ninja.responses import codes_4xx

from users.models import AuthUser, RefreshToken
from users.schemas import TelegramLoginIn, TokenPairOut, VerifyOut, RefreshIn, MessageOut
from users.telegram_initdata import verify_telegram_init_data
from users.jwt_utils import make_access_token, make_refresh_token, verify_jwt_token

api = NinjaAPI(title="Auth Service", version="1.0.0")

router = Router(tags=["Auth"])
internal = Router(tags=["Internal"])


def _parse_user_from_pairs(pairs: dict) -> dict:
    user_raw = pairs.get("user")
    user = json.loads(user_raw) if user_raw else {}
    return {
        "telegram_id": int(user.get("id")),
        "username": user.get("username"),
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "photo_url": user.get("photo_url"),
    }


@router.post("/telegram/login", response={200: TokenPairOut, codes_4xx: MessageOut})
def telegram_login(request, payload: TelegramLoginIn):
    ok, pairs = verify_telegram_init_data(payload.initData, settings.TG_BOT_TOKEN)
    if not ok:
        return 401, {"message": "Invalid Telegram initData signature"}

    if "auth_date" not in pairs or "user" not in pairs:
        return 400, {"message": "Invalid initData payload", "details": {"missing": ["auth_date", "user"]}}

    user_data = _parse_user_from_pairs(pairs)
    if not user_data.get("telegram_id"):
        return 400, {"message": "Invalid user payload"}

    auth_date = datetime.fromtimestamp(int(pairs["auth_date"]), tz=timezone.utc)

    with transaction.atomic():
        u, _created = AuthUser.objects.update_or_create(
            telegram_id=user_data["telegram_id"],
            defaults={
                "username": user_data.get("username"),
                "first_name": user_data.get("first_name"),
                "last_name": user_data.get("last_name"),
                "photo_url": user_data.get("photo_url"),
                "auth_date": auth_date,
                "is_active": True,
            },
        )

        access_token, access_ttl = make_access_token(
            user_id=str(u.id),
            private_key_pem=settings.JWT_PRIVATE_KEY,
            issuer=settings.JWT_ISSUER,
            ttl_seconds=settings.JWT_ACCESS_TTL,
        )
        refresh_token, refresh_ttl = make_refresh_token(
            user_id=str(u.id),
            private_key_pem=settings.JWT_PRIVATE_KEY,
            issuer=settings.JWT_ISSUER,
            ttl_seconds=settings.JWT_REFRESH_TTL,
        )

        RefreshToken.objects.create(
            user=u,
            token=refresh_token,
            revoked=False,
            expires_at=dj_tz.now() + timedelta(seconds=refresh_ttl),
        )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": access_ttl,
        "user_id": str(u.id),
    }


@router.post("/refresh", response={200: TokenPairOut, codes_4xx: MessageOut})
def refresh(request, payload: RefreshIn):
    token = payload.refresh_token.strip()
    user_id = verify_jwt_token(token, settings.JWT_PUBLIC_KEY, issuer=settings.JWT_ISSUER, required_type="refresh")
    if not user_id:
        return 401, {"message": "Invalid refresh token"}

    rt = RefreshToken.objects.filter(token=token, revoked=False).select_related("user").first()
    if not rt:
        return 401, {"message": "Refresh token revoked/unknown"}
    if rt.expires_at < dj_tz.now():
        return 401, {"message": "Refresh token expired"}

    access_token, access_ttl = make_access_token(
        user_id=user_id,
        private_key_pem=settings.JWT_PRIVATE_KEY,
        issuer=settings.JWT_ISSUER,
        ttl_seconds=settings.JWT_ACCESS_TTL,
    )
    new_refresh, refresh_ttl = make_refresh_token(
        user_id=user_id,
        private_key_pem=settings.JWT_PRIVATE_KEY,
        issuer=settings.JWT_ISSUER,
        ttl_seconds=settings.JWT_REFRESH_TTL,
    )

    with transaction.atomic():
        rt.revoked = True
        rt.save(update_fields=["revoked"])
        RefreshToken.objects.create(
            user=rt.user,
            token=new_refresh,
            revoked=False,
            expires_at=dj_tz.now() + timedelta(seconds=refresh_ttl),
        )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh,
        "expires_in": access_ttl,
        "user_id": user_id,
    }


@internal.get("/verify", response=VerifyOut)
def internal_verify(request):
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "").strip()
    if not token:
        return {"valid": False}

    user_id = verify_jwt_token(token, settings.JWT_PUBLIC_KEY, issuer=settings.JWT_ISSUER, required_type="access")
    if not user_id:
        return {"valid": False}

    if not AuthUser.objects.filter(id=user_id, is_active=True).exists():
        return {"valid": False}

    return {"valid": True, "user_id": user_id}


api.add_router("", router)
api.add_router("/internal", internal)
