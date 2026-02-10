from abc import ABC, abstractmethod
from typing import Optional
from domain.library.entities.member import Member

class MemberRepository(ABC):

    @abstractmethod
    def get_by_id(self, member_id) -> Optional[Member]:
        pass

    @abstractmethod
    def get_by_email(self, email) -> Optional[Member]:
        pass

    @abstractmethod
    def delete(self, member_id) -> None:
        pass