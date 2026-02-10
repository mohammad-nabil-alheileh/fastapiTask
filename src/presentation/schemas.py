from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional


class MemberCreate(BaseModel):
    name: str
    email: EmailStr


class MemberResponse(BaseModel):
    member_id: UUID
    name: str
    email: EmailStr


class BookCreate(BaseModel):
    book_id: int
    title: str
    author: str


class BookResponse(BaseModel):
    book_id: int
    title: str
    author: str
    is_borrowed: bool
    borrowed_by: Optional[UUID]
    borrowed_date: Optional[datetime]


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None


class MemberUpdate(BaseModel):
    name: Optional[str] = None
