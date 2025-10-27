from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings
from app.core.constants import DatabaseConfig

# Convert postgres:// to postgresql+asyncpg://
async_database_url = settings.database_url.replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Async database engine
async_engine = create_async_engine(
    async_database_url,
    pool_size=DatabaseConfig.POOL_SIZE,
    max_overflow=DatabaseConfig.MAX_OVERFLOW,
    pool_pre_ping=DatabaseConfig.POOL_PRE_PING,
    pool_recycle=DatabaseConfig.POOL_RECYCLE,
    echo=DatabaseConfig.ECHO_SQL,
    connect_args={"statement_timeout": DatabaseConfig.STATEMENT_TIMEOUT},
)

AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_db():
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
