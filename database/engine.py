from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
import os
from dotenv.main import load_dotenv

def __setup():
    load_dotenv(".env")
    user = os.environ["PG_USER"]
    password = os.environ["PG_PASSWORD"]
    return create_async_engine(f"postgresql+asyncpg://localhost:5432/tomato?user={user}&password={password}", echo=False), create_engine(f"postgresql://localhost:5432/tomato?user={user}&password={password}")

async_engine, sync_engine = __setup()