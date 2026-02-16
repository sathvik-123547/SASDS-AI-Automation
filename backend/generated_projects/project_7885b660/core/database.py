from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from core.config import settings

# Create an async SQLAlchemy engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create an async session maker
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base class for our ORM models
Base = declarative_base()

async def get_db() -> AsyncSession:
    """
    Dependency to provide a database session.
    Yields an AsyncSession and ensures it's closed after use.
    """
    async with async_session_maker() as session:
        yield session
