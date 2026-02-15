from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


class MemberCreate(BaseModel):
    name: str
    email: EmailStr


class MemberResponse(BaseModel):
    member_id: UUID
    name: str
    email: EmailStr


class MemberUpdate(BaseModel):
    name: Optional[str] = None
