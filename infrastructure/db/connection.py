from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

engine = create_async_engine(
    "postgresql+asyncpg://mohammadNabil:mohammad1234DB@localhost:5433/library_db",
    echo=True
)

Base = declarative_base()