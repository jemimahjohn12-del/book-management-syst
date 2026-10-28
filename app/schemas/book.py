from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=150)
    publication_year: int | None = None
    price: float = Field(ge=0)
    available: bool = True


class BookResponse(BookBase):
    id: int