from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, crud, dependencies

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    # Vérifier que le livre existe
    book = crud.get_book(db, review.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.create_review(db, user_id=current_user.id, review=review)

@router.get("/book/{book_id}", response_model=List[schemas.Review])
def get_reviews_for_book(book_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.get_reviews_by_book(db, book_id)

@router.put("/{review_id}", response_model=schemas.Review)
def update_review(
    review_id: int,
    review_update: schemas.ReviewUpdate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    db_review = crud.get_review_by_id(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    if db_review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this review")
    return crud.update_review(db, db_review, review_update)

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    db_review = crud.get_review_by_id(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    if db_review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")
    crud.delete_review(db, db_review)
    return None 