from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.db.connection import Base
import uuid

class BookModel(Base):
    __tablename__ = "books"

    book_id = Column(UUID, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)

    borrowed_by = Column(UUID(as_uuid=True), ForeignKey("members.member_id"), nullable=True)
    borrowed_date = Column(DateTime(timezone = True), nullable=True)
    is_borrowed = Column(Boolean, nullable=False, default=False)


class MemberModel(Base):
    __tablename__ = "members"

    member_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
