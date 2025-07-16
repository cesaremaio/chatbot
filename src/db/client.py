from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.app_settings import settings

from typing import AsyncGenerator


URL = str(settings.database_url)

engine: AsyncEngine = create_async_engine(URL, echo=True)  # type hint here

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


Base = declarative_base()