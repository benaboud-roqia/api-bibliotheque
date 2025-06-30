from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    cover_url: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int
    owner_id: Optional[int]

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    books: List[Book] = []

    class Config:
        orm_mode = True

# Schémas pour les emprunts
class BorrowBase(BaseModel):
    book_id: int

class BorrowCreate(BorrowBase):
    pass

class Borrow(BorrowBase):
    id: int
    user_id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Schémas pour les commentaires/notes
class ReviewBase(BaseModel):
    book_id: int
    comment: Optional[str] = None
    rating: int

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    comment: Optional[str] = None
    rating: Optional[int] = None

class Review(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True 