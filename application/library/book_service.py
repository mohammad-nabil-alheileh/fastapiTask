class BookService:
    def __init__(self, book_repo, member_repo):
        self.book_repo = book_repo
        self.member_repo = member_repo

    async def create_book(self, book):
        existing = await self.book_repo.get_by_id(book.book_id)
        if existing:
            raise Exception("Book already exists")

        await self.book_repo.create(book)
        return book

    async def borrow_book(self, book_id: int, member_id):
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise Exception("Book not found")

        member = await self.member_repo.get_by_id(member_id)
        if not member:
            raise Exception("Member not found")

        book.borrow(member_id)
        await self.book_repo.update_state(book)
        return book

    async def get_book_by_id(self, book_id: int):
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise Exception("Book not found")

        return book

    async def return_book(self, book_id: int):
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise Exception("Book not found")

        book.return_book()
        await self.book_repo.update_state(book)
        return book

    async def list_books(self):
        return await self.book_repo.list()

    async def update_book(self, book_id, data):
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise Exception("Book not found")

        if data.title is not None:
            book.title = data.title

        if data.author is not None:
            book.author = data.author

        await self.book_repo.update(book)
        return book

    async def delete_book(self, book_id):
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise Exception("Book not found")

        await self.book_repo.delete(book_id)
