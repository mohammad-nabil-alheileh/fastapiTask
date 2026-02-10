from sqlalchemy import Table, Column, String, Integer, Boolean, DateTime, MetaData, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

books = Table(
    "books",
    metadata,
    Column("book_id", Integer, primary_key = True),
    Column("title", String, nullable=False),
    Column("author", String, nullable=False),
    Column("borrowed_by", UUID, ForeignKey("members.member_id"), nullable=True),
    Column("borrowed_date", DateTime, nullable=True),
    Column("is_borrowed", Boolean, default=False),
)

members = Table(
    "members",
    metadata,
    Column("member_id", UUID, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False, unique=True)
)