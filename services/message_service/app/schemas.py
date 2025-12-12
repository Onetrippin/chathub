from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ConversationOut(BaseModel):
    id: str
    user_id: str
    platform: str
    external_chat_id: Optional[str] = None
    created_at: datetime


class MessageOut(BaseModel):
    id: str
    conversation_id: str
    sender: str
    text: str
    timestamp: datetime
    is_ai_generated: bool


class SendMessageIn(BaseModel):
    user_id: str
    text: str = Field(min_length=1, max_length=5000)
    sender: str = "user"
