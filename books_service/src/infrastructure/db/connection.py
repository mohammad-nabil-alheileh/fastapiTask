from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool  # Add this import
from src.infrastructure.db.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)

Base = declarative_base()