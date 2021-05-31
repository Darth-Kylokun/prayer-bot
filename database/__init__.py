import asyncio
from database.tables import Base
from .engine import sync_engine, async_engine
from .tables import Base, Prefixes, Entitys, Prayers
from sqlalchemy.orm import Session

def __setup():
    Base.metadata.create_all(sync_engine)

    ses = Session(sync_engine)

    return ses

session = __setup()