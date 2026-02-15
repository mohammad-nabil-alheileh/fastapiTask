from src.application.library.book_service import BookService
from src.infrastructure.repositories.book_repo_sql import BookRepositorySQL
from src.infrastructure.repositories.member_repo_sql import MemberRepositorySQL


def get_book_service() -> BookService:
    book_repo = BookRepositorySQL()
    member_repo = MemberRepositorySQL()
    return BookService(book_repo, member_repo)

def get_member_repository():
    return MemberRepositorySQL()