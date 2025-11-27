from datetime import datetime

from pydantic import BaseModel, Field
from bson import ObjectId


class ConversationCache(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias='_id')
    conversation_id: str
    last_messages: list[dict] = []
    updated_at: datetime = Field(default_factory=datetime.now)
