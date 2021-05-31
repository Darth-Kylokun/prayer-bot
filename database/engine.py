from sqlalchemy.ext.asyncio import create_async_engine
import os

password = os.environ["PG_PASSWORD"]

engine = create_async_engine(f"postgresql+asyncpg://localhost:5432/tomato?user=darth&password={password}", echo=False)