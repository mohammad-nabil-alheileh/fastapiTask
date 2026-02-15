from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, TypeAlias
from uuid import UUID, uuid4
from src.presentation.schemas import BookCreate, BookResponse, BookUpdate
from src.presentation.dependencies import get_book_service
from src.domain.library.entities.book import Book
from src.application.library.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])
BookServiceDep: TypeAlias = Annotated[BookService, Depends(get_book_service)]

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_books( data: BookCreate, service: BookServiceDep):
    book = Book(uuid4(), data.title, data.author)
    try:
        creted_book = service.create_book(book)
        return await creted_book
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model= list[BookResponse], status_code=status.HTTP_200_OK)
async def get_all_books(service: BookServiceDep):
    books = service.list_books()
    return await books


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: UUID, service: BookServiceDep):
    try: 
        return await service.get_book_by_id(book_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book( book_id: UUID, data: BookUpdate, serivce: BookServiceDep):
    try:
        return await serivce.update_book(book_id, data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, service: BookServiceDep):
    try:
        await service.delete_book(book_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{book_id}/borrow/member/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def borrow_book(book_id:UUID, member_id: UUID, service: BookServiceDep):
    try:
        await service.borrow_book(book_id,member_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

@router.post("/{book_id}/return", status_code=status.HTTP_204_NO_CONTENT)
async def return_book(book_id: UUID, service: BookServiceDep):
    try:
        await service.return_book(book_id)
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))
