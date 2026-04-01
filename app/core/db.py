from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from core.config import settings

Base = declarative_base()
engine: AsyncEngine = create_async_engine(
    settings.database_url, echo=settings.DEBUG
)

AsyncSession = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSession() as session:
        yield session