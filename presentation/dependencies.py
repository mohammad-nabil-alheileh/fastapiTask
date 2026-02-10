from application.library.book_service import BookService
from application.library.member_service import MemberService
from infrastructure.repositories.book_repo_sql import BookRepositorySQL
from infrastructure.repositories.member_repo_sql import MemberRepositorySQL


def get_book_service() -> BookService:
    book_repo = BookRepositorySQL()
    member_repo = MemberRepositorySQL()
    return BookService(book_repo, member_repo)


def get_member_service() -> MemberService:
    member_repo = MemberRepositorySQL()
    return MemberService(member_repo)