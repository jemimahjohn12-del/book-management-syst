from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Response, status

from app.models import book as book_model
from app.schemas.book import BookBase, BookResponse

router = APIRouter(prefix="/books", tags=["books"])

# Must be a positive integer that fits in a Postgres INTEGER
BookId = Annotated[int, Path(gt=0, le=2_147_483_647)]


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookBase):
    return book_model.create_book(book.model_dump())


@router.get("", response_model=list[BookResponse])
def list_books():
    return book_model.get_all_books()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: BookId):
    book = book_model.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: BookId, book: BookBase):
    updated = book_model.update_book(book_id, book.model_dump())
    if updated is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: BookId):
    if not book_model.delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)