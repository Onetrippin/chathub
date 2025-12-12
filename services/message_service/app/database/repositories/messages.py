from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Message, Conversation

async def list_messages(db: AsyncSession, conversation_id: str, limit: int = 100) -> list[Message]:
    res = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp.desc())
        .limit(limit)
    )
    items = list(res.scalars().all())
    return list(reversed(items))

async def add_message(
    db: AsyncSession,
    conversation_id: str,
    sender: str,
    text: str,
    is_ai_generated: bool = False,
) -> Message:
    res = await db.execute(select(Conversation.id).where(Conversation.id == conversation_id))
    if res.scalar_one_or_none() is None:
        raise ValueError("Conversation not found")

    m = Message(
        conversation_id=conversation_id,
        sender=sender,
        text=text,
        is_ai_generated=is_ai_generated,
    )
    db.add(m)
    await db.commit()
    await db.refresh(m)
    return m
