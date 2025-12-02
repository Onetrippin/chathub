import uuid
from datetime import datetime, UTC

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base import Base


class Conversation(Base):
    __tablename__ = 'conversation'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    platform = Column(String(32), nullable=False)
    external_chat_id = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))

    messages = relationship('Message', back_populates='conversation')
