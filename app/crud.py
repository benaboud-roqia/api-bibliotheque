from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, auth

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role if hasattr(user, 'role') and user.role else "user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 10, author: Optional[str] = None, title: Optional[str] = None, keyword: Optional[str] = None) -> List[models.Book]:
    query = db.query(models.Book)
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if keyword:
        query = query.filter(models.Book.description.ilike(f"%{keyword}%"))
    return query.offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate, user_id: int) -> models.Book:
    db_book = models.Book(**book.dict(), owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, db_book: models.Book, book_update: schemas.BookUpdate) -> models.Book:
    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, db_book: models.Book):
    db.delete(db_book)
    db.commit()

def create_borrow(db: Session, user_id: int, book_id: int) -> models.Borrow:
    db_borrow = models.Borrow(user_id=user_id, book_id=book_id)
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow

def return_borrow(db: Session, borrow_id: int) -> Optional[models.Borrow]:
    db_borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if db_borrow and db_borrow.return_date is None:
        from datetime import datetime
        db_borrow.return_date = datetime.utcnow()
        db.commit()
        db.refresh(db_borrow)
    return db_borrow

def get_borrow_by_id(db: Session, borrow_id: int) -> Optional[models.Borrow]:
    return db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()

def get_borrows_by_user(db: Session, user_id: int) -> List[models.Borrow]:
    return db.query(models.Borrow).filter(models.Borrow.user_id == user_id).all()

def get_all_borrows(db: Session) -> List[models.Borrow]:
    return db.query(models.Borrow).all()

def create_review(db: Session, user_id: int, review: schemas.ReviewCreate) -> models.Review:
    db_review = models.Review(user_id=user_id, book_id=review.book_id, comment=review.comment, rating=review.rating)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_by_book(db: Session, book_id: int) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.book_id == book_id).all()

def get_review_by_id(db: Session, review_id: int) -> Optional[models.Review]:
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def update_review(db: Session, db_review: models.Review, review_update: schemas.ReviewUpdate) -> models.Review:
    for key, value in review_update.dict(exclude_unset=True).items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, db_review: models.Review):
    db.delete(db_review)
    db.commit() 