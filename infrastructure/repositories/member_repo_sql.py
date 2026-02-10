from domain.library.repositories.member_repository import MemberRepository
from domain.library.entities.member import Member
from infrastructure.db.session import db_async_session
from infrastructure.db.models import MemberModel
from sqlalchemy import select


class MemberRepositorySQL(MemberRepository):

    async def get_by_id(self, member_id):
        async with db_async_session() as db:
            result = await db.execute(
                select(MemberModel).where(MemberModel.member_id == member_id)
            )
            row = result.scalars().first()

            if not row:
                return None

            return Member(row.member_id, row.name, row.email)

    async def get_by_email(self, email):
        async with db_async_session() as db:
            result = await db.execute(
                select(MemberModel).where(MemberModel.email == email)
            )
            row = result.scalars().first()

            if not row:
                return None

            return Member(row.member_id, row.name, row.email)

    async def list(self):
        async with db_async_session() as db:
            result = await db.execute(select(MemberModel))
            rows = result.scalars().all()

            members = []
            for row in rows:
                members.append(
                    Member(
                        member_id=row.member_id,
                        name=row.name,
                        email=row.email,
                    )
                )

            return members

    async def create(self, member: Member):
        async with db_async_session() as db:
            db.add(
                MemberModel(
                    member_id=member.member_id,
                    name=member.name,
                    email=member.email,
                )
            )

    async def update(self, member: Member):
        async with db_async_session() as db:
            result = await db.execute(
                select(MemberModel).where(MemberModel.member_id == member.member_id)
            )
            row = result.scalars().first()

            if not row:
                return

            row.name = member.name

    async def delete(self, member_id):
        async with db_async_session() as db:
            result = await db.execute(
                select(MemberModel).where(MemberModel.member_id == member_id)
            )
            row = result.scalars().first()

            if row:
                await db.delete(row)
