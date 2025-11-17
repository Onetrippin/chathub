from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Integration


async def list_integrations(session: AsyncSession, user_id: int) -> list[Integration]:
    res = await session.execute(select(Integration).where(Integration.user_id == user_id).order_by(Integration.platform))
    return list(res.scalars().all())


async def seed_integrations(session: AsyncSession, user_id: int) -> None:
    existing = await list_integrations(session, user_id)
    if existing:
        return
    session.add_all([
        Integration(user_id=user_id, platform="telegram", status="connected", last_sync_at=datetime.utcnow()),
        Integration(user_id=user_id, platform="gmail", status="connected", last_sync_at=datetime.utcnow()),
        Integration(user_id=user_id, platform="notion", status="disconnected", last_sync_at=None),
        Integration(user_id=user_id, platform="gcal", status="connected", last_sync_at=datetime.utcnow()),
    ])
    await session.commit()
