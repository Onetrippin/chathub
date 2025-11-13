from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Integer, BigInteger, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("telegram_id", name="uq_users_telegram_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(128), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow)

    settings: Mapped["UserSettings"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    integrations: Mapped[list["Integration"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    files: Mapped[list["FileMeta"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    ai_history: Mapped[list["AIHistory"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    theme: Mapped[str] = mapped_column(String(16), default="dark")
    language: Mapped[str] = mapped_column(String(8), default="ru")
    timezone: Mapped[str] = mapped_column(String(64), default="Europe/Moscow")
    ai_persona: Mapped[str] = mapped_column(String(64), default="Коротко и по делу")
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship(back_populates="settings")


class Integration(Base):
    __tablename__ = "integrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    platform: Mapped[str] = mapped_column(String(32))   # telegram/gmail/notion...
    status: Mapped[str] = mapped_column(String(16), default="connected")  # connected/disconnected
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)

    user: Mapped["User"] = relationship(back_populates="integrations")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    type: Mapped[str] = mapped_column(String(32))  # ai_ready/sync_error/new_message...
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="notifications")


class FileMeta(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    filename: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[str] = mapped_column(String(32), default="document")
    size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    url: Mapped[str] = mapped_column(Text, default="s3://bucket/key")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="files")


class AIHistory(Base):
    __tablename__ = "ai_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    prompt: Mapped[str] = mapped_column(Text)
    response: Mapped[str] = mapped_column(Text)
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="ai_history")
