from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID, uuid4
from typing import Annotated, TypeAlias
from presentation.schemas import MemberCreate, MemberResponse, MemberUpdate
from presentation.dependencies import get_member_service
from domain.library.entities.member import Member
from application.library.member_service import MemberService


router = APIRouter(prefix="/members", tags=["Members"])
MemberServiceDep: TypeAlias = Annotated[MemberService, Depends(get_member_service)]

@router.post("/members/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
async def create_member( data: MemberCreate, service: MemberServiceDep):
    member = Member(uuid4(), data.name, data.email)
    try:
        member_created = await service.create_member(member)
        return member_created
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.get("/members/", response_model=list[MemberResponse], status_code=status.HTTP_200_OK)
async def get_all_members(service: MemberServiceDep):
    members = service.list_members()
    return await members

@router.get("/members/{member_id}", response_model=MemberResponse, status_code=status.HTTP_200_OK)
async def get_member_by_id(member_id: UUID, service: MemberServiceDep):
    try:
        return await service.get_member_by_id(member_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

@router.put("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_member(member_id: UUID, data: MemberUpdate, service: MemberServiceDep):
    try:
        return await service.update_member(member_id, data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

@router.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_member(member_id: UUID, service: MemberServiceDep):
    try:
        return await service.delete_member_by_id(member_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))