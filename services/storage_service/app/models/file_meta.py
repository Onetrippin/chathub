from datetime import datetime

from pydantic import BaseModel, Field
from bson import ObjectId


class FileMeta(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias='_id')
    user_id: str
    message_id: str
    file_type: str
    file_url: str
    size: int
    created_at: datetime = Field(default_factory=datetime.now)
