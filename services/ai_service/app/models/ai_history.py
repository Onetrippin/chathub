import uuid
from datetime import datetime, UTC

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from db.base import Base


class AIHistory(Base):
    __tablename__ = 'ai_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    prompt = Column(String, nullable=False)
    response = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
