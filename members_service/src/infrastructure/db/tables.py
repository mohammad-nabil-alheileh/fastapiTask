from sqlalchemy import Table, Column, String, MetaData 
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

members = Table(
    "members",
    metadata,
    Column("member_id", UUID, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False, unique=True)
)