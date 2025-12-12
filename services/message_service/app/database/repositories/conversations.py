from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Conversation

async def list_conversations(db: AsyncSession, user_id: str) -> list[Conversation]:
    res = await db.execute(
        select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc())
    )
    return list(res.scalars().all())

async def get_conversation(db: AsyncSession, conversation_id: str) -> Conversation | None:
    res = await db.execute(select(Conversation).where(Conversation.id == conversation_id))
    return res.scalar_one_or_none()

async def create_conversation(db: AsyncSession, user_id: str, platform: str = "telegram") -> Conversation:
    c = Conversation(user_id=user_id, platform=platform)
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return c
