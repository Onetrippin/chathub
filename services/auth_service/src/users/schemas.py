from ninja import Schema
from typing import Optional, Dict, Any


class TelegramLoginIn(Schema):
    initData: str


class TokenPairOut(Schema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    user_id: str


class VerifyOut(Schema):
    valid: bool
    user_id: Optional[str] = None


class RefreshIn(Schema):
    refresh_token: str


class MessageOut(Schema):
    message: str
    details: Optional[Dict[str, Any]] = None
