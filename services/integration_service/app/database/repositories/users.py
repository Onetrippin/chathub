from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, UserSettings


async def upsert_user(
    session: AsyncSession,
    telegram_id: int,
    username: str | None,
    first_name: str | None,
    last_name: str | None,
) -> User:
    res = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = res.scalar_one_or_none()

    if user is None:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            last_seen_at=datetime.utcnow(),
        )
        session.add(user)
        await session.flush()  # получить user.id

        # settings по умолчанию
        session.add(UserSettings(user_id=user.id))
        await session.commit()
        await session.refresh(user)
        return user

    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.last_seen_at = datetime.utcnow()
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_tg(session: AsyncSession, telegram_id: int) -> User | None:
    res = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return res.scalar_one_or_none()


async def delete_user_by_tg(session: AsyncSession, telegram_id: int) -> None:
    user = await get_user_by_tg(session, telegram_id)
    if user:
        await session.delete(user)
        await session.commit()
