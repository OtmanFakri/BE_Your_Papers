import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

user: str = os.environ.get("USER_DB")
password: str = os.environ.get("PASSWORD_DB")
host: str = os.environ.get("HOST")
dbname: str = os.environ.get("DB_NAME")

SQLALCHMEY_DB_URL = f"postgresql+asyncpg://{user}:{password}@{host}:5432/{dbname}"

engine = create_async_engine(SQLALCHMEY_DB_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
