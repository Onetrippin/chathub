from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from bot.config import DB_DSN
from database.models import Base

engine = create_async_engine(DB_DSN, echo=False, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
