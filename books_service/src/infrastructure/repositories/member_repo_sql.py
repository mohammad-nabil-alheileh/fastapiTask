from uuid import UUID
from sqlalchemy import select, insert
from src.domain.library.entities.member import Member
from src.domain.library.repositories.member_repository import MemberRepository
from src.infrastructure.db.session import db_async_session
from src.infrastructure.db.tables import members


class MemberRepositorySQL(MemberRepository):

    async def create(self, member: Member):
        async with db_async_session() as session:
            stmt = insert(members).values(member_id=member.member_id)
            await session.execute(stmt)
            await session.commit()
            return member

    async def get_by_id(self, member_id: UUID):
        async with db_async_session() as session:
            stmt = select(members).where(members.c.member_id == member_id)
            result = await session.execute(stmt)
            row = result.first()

            if row:
                return Member(row.member_id)

            return None
