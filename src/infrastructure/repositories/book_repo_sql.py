from domain.library.repositories.book_repository import BookRepository
from domain.library.entities.book import Book
from infrastructure.db.session import db_async_session
from infrastructure.db.models import BookModel
from sqlalchemy import select


class BookRepositorySQL(BookRepository):

    async def get_by_id(self, book_id: int):
        async with db_async_session() as db:
            result = await db.execute(
                select(BookModel).where(BookModel.book_id == book_id)
            )
            row = result.scalars().first()

            if not row:
                return None

            book = Book(
                book_id=row.book_id,
                title=row.title,
                author=row.author,
            )
            book.borrowed_by = row.borrowed_by
            book.borrowed_date = row.borrowed_date

            return book

    async def list(self):
        async with db_async_session() as db:
            result = await db.execute(select(BookModel))
            rows = result.scalars().all()

            books = []
            for row in rows:
                book = Book(
                    book_id=row.book_id,
                    title=row.title,
                    author=row.author,
                )
                book.borrowed_by = row.borrowed_by
                book.borrowed_date = row.borrowed_date
                books.append(book)

            return books

    async def create(self, book: Book):
        async with db_async_session() as db:
            db.add(
                BookModel(
                    book_id=book.book_id,
                    title=book.title,
                    author=book.author,
                    borrowed_by=None,
                    borrowed_date=None,
                    is_borrowed=False,
                )
            )

    async def update(self, book: Book):
        async with db_async_session() as db:
            result = await db.execute(
                select(BookModel).where(BookModel.book_id == book.book_id)
            )
            row = result.scalars().first()

            if not row:
                return

            row.title = book.title
            row.author = book.author

    async def update_state(self, book: Book):
        async with db_async_session() as db:
            result = await db.execute(
                select(BookModel).where(BookModel.book_id == book.book_id)
            )
            row = result.scalars().first()

            if not row:
                return

            row.borrowed_by = book.borrowed_by
            row.borrowed_date = book.borrowed_date
            row.is_borrowed = book.borrowed_by is not None

    async def delete(self, book_id: int):
        async with db_async_session() as db:
            result = await db.execute(
                select(BookModel).where(BookModel.book_id == book_id)
            )
            row = result.scalars().first()

            if row:
                await db.delete(row)
