from .tables import Base, Entitys, Prayers, Prefixes
from .engine import async_engine, sync_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

async def _setup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    ses = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

    return ses

coro_session = _setup()
session = Session(sync_engine)