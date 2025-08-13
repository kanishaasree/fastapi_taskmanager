# import os
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = os.getenv("DATABASE_URL", "LOCAL_DB_URL")

# engine = create_async_engine(DATABASE_URL, echo=True, future=True)
# AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# async def get_session():
#     async with AsyncSessionLocal() as session:
#         yield session

      
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


environment = os.getenv("ENVIRONMENT", "local")
if environment == "prod":
    db_url = os.getenv("DATABASE_URL")
else:
    db_url = os.getenv("LOCAL_DB_URL", "sqlite+aiosqlite:///./task.db")
if not db_url:
    raise RuntimeError("No database URL configured. Check your .env file.")

engine = create_async_engine(db_url, echo=True, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
