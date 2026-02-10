from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from infrastructure.db.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()