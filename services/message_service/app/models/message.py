import uuid
from datetime import datetime, UTC

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base import Base


class Message(Base):
    __tablename__ = 'message'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversation.id'))
    sender = Column(String(64))
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.now(UTC))
    is_ai_generated = Column(Boolean, default=False)

    conversation = relationship('Conversation', back_populates='messages')
