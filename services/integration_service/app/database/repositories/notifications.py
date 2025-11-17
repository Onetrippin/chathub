from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Notification


async def add_notification(session: AsyncSession, user_id: int, type_: str, payload: str) -> Notification:
    n = Notification(user_id=user_id, type=type_, payload=payload)
    session.add(n)
    await session.commit()
    await session.refresh(n)
    return n


async def last_notifications(session: AsyncSession, user_id: int, limit: int = 5) -> list[Notification]:
    res = await session.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.id.desc())
        .limit(limit)
    )
    return list(res.scalars().all())


async def seed_notifications(session: AsyncSession, user_id: int) -> None:
    items = await last_notifications(session, user_id, limit=1)
    if items:
        return
    await add_notification(session, user_id, "ai_ready", "AI ответ готов: черновик ТЗ сформирован.")
    await add_notification(session, user_id, "new_message", "Входящее: «Привет! Проверишь дизайн?»")
    await add_notification(session, user_id, "sync_ok", "Gmail синхронизирован без ошибок.")
