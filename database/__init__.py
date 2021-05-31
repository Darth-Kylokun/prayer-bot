from .tables import Base, Entitys, Prayers
from .engine import engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

async def _setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    ses = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    return ses

coro_session = _setup()
