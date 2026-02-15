from abc import ABC, abstractmethod
from uuid import UUID
from src.domain.library.entities.member import Member

class MemberRepository(ABC):

    @abstractmethod
    async def create(self, member: Member):
        pass

    @abstractmethod
    async def get_by_id(self, member_id: UUID):
        pass
