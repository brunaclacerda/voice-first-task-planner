from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from ..core.logging import setup_logger
from .config import get_settings

logger = setup_logger(__name__)


class Base(DeclarativeBase):
    """Base class"""


asyncio_engine = create_async_engine(get_settings().database_url)
AsyncSessionLocal = async_sessionmaker(bind=asyncio_engine, expire_on_commit=False)


async def init_db() -> None:
    """It will be removed once migrations are implemented."""
    async with asyncio_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
