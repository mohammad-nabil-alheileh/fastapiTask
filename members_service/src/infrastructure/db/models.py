from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from src.infrastructure.db.connection import Base
import uuid

class MemberModel(Base):
    __tablename__ = "members"

    member_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
