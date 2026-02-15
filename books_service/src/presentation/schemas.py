from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str


class BookResponse(BaseModel):
    book_id: UUID
    title: str
    author: str
    is_borrowed: bool
    borrowed_by: Optional[UUID]
    borrowed_date: Optional[datetime]


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

