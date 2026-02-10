from datetime import datetime, timezone


class Book:
    def __init__(self, book_id: int, title: str, author: str):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.borrowed_by = None
        self.borrowed_date = None

    @property
    def is_borrowed(self) -> bool:
        return self.borrowed_by is not None

    def borrow(self, member_id):
        if self.is_borrowed:
            raise Exception("Book is already borrowed")

        self.borrowed_by = member_id
        self.borrowed_date = datetime.now(timezone.utc)

    def return_book(self):
        if not self.is_borrowed:
            raise Exception("Book is not borrowed")

        self.borrowed_by = None
        self.borrowed_date = None