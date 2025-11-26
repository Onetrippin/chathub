import uuid
from datetime import datetime, UTC

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID

from db.base import Base


class AIContext(Base):
    __tablename__ = 'ai_context'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    last_prompt = Column(String, nullable=True)
    last_response = Column(String, nullable=True)
    tokens_used = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.now(UTC))
