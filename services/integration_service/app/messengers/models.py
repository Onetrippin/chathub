from pydantic import BaseModel, Field
from typing import Literal, Dict, Any
from datetime import datetime


Platform = Literal["vk", "telegram_user", "telegram_bot"]


class InboundMessageEvent(BaseModel):
    platform: Platform
    user_id: str
    external_chat_id: str
    external_message_id: str
    sender_external_id: str
    text: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    raw: Dict[str, Any] = Field(default_factory=dict)


class OutboundMessageCommand(BaseModel):
    platform: Platform
    user_id: str
    external_chat_id: str
    text: str
    meta: Dict[str, Any] = Field(default_factory=dict)
