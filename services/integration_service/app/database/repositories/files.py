from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import FileMeta


async def list_files(session: AsyncSession, user_id: int, limit: int = 10) -> list[FileMeta]:
    res = await session.execute(
        select(FileMeta)
        .where(FileMeta.user_id == user_id)
        .order_by(FileMeta.id.desc())
        .limit(limit)
    )
    return list(res.scalars().all())


async def seed_files(session: AsyncSession, user_id: int) -> None:
    existing = await list_files(session, user_id, limit=1)
    if existing:
        return
    session.add_all([
        FileMeta(user_id=user_id, filename="contract.pdf", file_type="document", size_bytes=428_114, url="s3://files/contract.pdf"),
        FileMeta(user_id=user_id, filename="avatar.png", file_type="image", size_bytes=96_443, url="s3://files/avatar.png"),
        FileMeta(user_id=user_id, filename="voice_2025-12-18.ogg", file_type="audio", size_bytes=1_245_101, url="s3://files/voice_2025-12-18.ogg"),
    ])
    await session.commit()
