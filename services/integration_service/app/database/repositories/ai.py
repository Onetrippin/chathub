from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import AIHistory


async def add_ai_history(session: AsyncSession, user_id: int, prompt: str, response: str, tokens_used: int = 180) -> AIHistory:
    row = AIHistory(user_id=user_id, prompt=prompt, response=response, tokens_used=tokens_used)
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return row


async def last_ai(session: AsyncSession, user_id: int) -> AIHistory | None:
    res = await session.execute(
        select(AIHistory).where(AIHistory.user_id == user_id).order_by(AIHistory.id.desc()).limit(1)
    )
    return res.scalars().first()
