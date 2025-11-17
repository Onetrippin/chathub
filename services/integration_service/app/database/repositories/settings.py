from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import UserSettings


async def get_settings(session: AsyncSession, user_id: int) -> UserSettings:
    res = await session.execute(select(UserSettings).where(UserSettings.user_id == user_id))
    settings = res.scalar_one()
    return settings


async def toggle_theme(session: AsyncSession, user_id: int) -> UserSettings:
    settings = await get_settings(session, user_id)
    settings.theme = "light" if settings.theme == "dark" else "dark"
    await session.commit()
    await session.refresh(settings)
    return settings


async def toggle_notifications(session: AsyncSession, user_id: int) -> UserSettings:
    settings = await get_settings(session, user_id)
    settings.notifications_enabled = not settings.notifications_enabled
    await session.commit()
    await session.refresh(settings)
    return settings
