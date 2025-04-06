from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, text
from typing import AsyncGenerator
from app.core.settings import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create async engine with connection pooling
engine: AsyncEngine = create_async_engine(
    settings.get_database_url,
    echo=settings.DEBUG,  # Controlled by environment settings
    pool_size=5,          # Default pool size, adjust as needed
    max_overflow=10,      # Allow extra connections under load
    pool_timeout=30,      # Timeout for acquiring connections
    pool_pre_ping=True    # Validate connections before use
)

# Create async session factory at module level
async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provide an async database session."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
            

async def init_db() -> None:
    """Initialize the database by creating all tables."""
    try:
        # Test connection
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1;"))
            logger.info(f"Database connection test: {result.scalar()}")

        # Create all tables
        async with engine.begin() as conn:
            ...
            '''Import all models here if not using alembic
               and uncomment the following lines
            '''
            # await conn.run_sync(SQLModel.metadata.create_all)
            # logger.info("Database tables created successfully")

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def shutdown_db() -> None:
    """Gracefully shutdown the database engine."""
    await engine.dispose()
    logger.info("Database engine disposed")
