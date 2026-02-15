from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID, uuid4
from typing import Annotated, TypeAlias
from src.presentation.schemas import MemberCreate, MemberResponse, MemberUpdate
from src.presentation.dependencies import get_member_service
from src.domain.library.entities.member import Member
from src.application.library.member_service import MemberService


router = APIRouter(prefix="/members", tags=["Members"])
MemberServiceDep: TypeAlias = Annotated[MemberService, Depends(get_member_service)]

@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member( data: MemberCreate, service: MemberServiceDep):
    member = Member(uuid4(), data.name, data.email)
    try:
        member_created = await service.create_member(member)
        return member_created
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.get("/", response_model=list[MemberResponse], status_code=status.HTTP_200_OK)
async def get_all_members(service: MemberServiceDep):
    return await service.list_members()

@router.get("/members/{member_id}", response_model=MemberResponse, status_code=status.HTTP_200_OK)
async def get_member_by_id(member_id: UUID, service: MemberServiceDep):
    try:
        return await service.get_member_by_id(member_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

@router.put("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_member(member_id: UUID, data: MemberUpdate, service: MemberServiceDep):
    try:
        await service.update_member(member_id, data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(member_id: UUID, service: MemberServiceDep):
    try:
        await service.delete_member_by_id(member_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))