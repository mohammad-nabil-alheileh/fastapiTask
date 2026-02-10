from uuid import UUID


class MemberService:

    def __init__(self, member_repo):
        self.member_repo = member_repo

    async def create_member(self, member):
        existing = await self.member_repo.get_by_email(member.email)
        if existing:
            raise Exception("Email already exists")
        
        await self.member_repo.create(member)
        return member
    

    async def update_member(self, member_id, data):
        member = await self.member_repo.get_by_id(member_id)
        if not member:
            raise Exception("Member not found")
        
        if data.name is not None:
            member.name = data.name

        await self.member_repo.update(member)
        return member

    async def list_members(self):
        return await self.member_repo.list()
    
    async def get_member_by_id(self, member_id: UUID):
        member = await self.member_repo.get_by_id(member_id)
        if not member:
            raise Exception("Member not found")
        
        return member

    async def delete_member_by_id(self, member_id: UUID):
        member = await self.member_repo.get_by_id(member_id)
        if not member:
            raise Exception("Member not found")
        
        await self.member_repo.delete(member_id)