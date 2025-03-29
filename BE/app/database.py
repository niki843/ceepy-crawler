from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from BE.app.config import DATABASE_URL

# Create Async Engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Session Local
async_session  = async_sessionmaker(bind=engine, expire_on_commit=False)

# Base Class
Base = declarative_base()

# Dependency function to get DB session
async def get_db():
    async with async_session() as session:
        yield session