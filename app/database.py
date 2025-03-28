from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Create Async Engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Session Local
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Base Class
Base = declarative_base()

# Dependency function to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session