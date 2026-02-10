from abc import ABC, abstractmethod
from typing import List, Optional
from domain.library.entities.book import Book

class BookRepository(ABC):

    @abstractmethod
    def get_by_id(self, book_id: int) ->Optional[Book]:
        pass

    @abstractmethod
    def list(self) -> List[Book]:
        pass

    @abstractmethod
    def create(self, book: Book) -> None:
        pass

    @abstractmethod
    def update(self, book: Book) -> None:
        pass

    @abstractmethod
    def delete(self, book_id: int) -> None:
        pass

