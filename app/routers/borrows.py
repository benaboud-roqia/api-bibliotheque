from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, crud, dependencies

router = APIRouter(prefix="/borrows", tags=["borrows"])

@router.post("/", response_model=schemas.Borrow, status_code=status.HTTP_201_CREATED)
def borrow_book(
    borrow: schemas.BorrowCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    # Vérifier que le livre existe
    book = crud.get_book(db, borrow.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Vérifier que le livre n'est pas déjà emprunté (non rendu)
    for b in book.borrows:
        if b.return_date is None:
            raise HTTPException(status_code=400, detail="Book already borrowed")
    return crud.create_borrow(db, user_id=current_user.id, book_id=borrow.book_id)

@router.post("/{borrow_id}/return", response_model=schemas.Borrow)
def return_book(
    borrow_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    db_borrow = crud.get_borrow_by_id(db, borrow_id)
    if not db_borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    if db_borrow.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to return this borrow")
    if db_borrow.return_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")
    return crud.return_borrow(db, borrow_id)

@router.get("/me", response_model=List[schemas.Borrow])
def get_my_borrows(
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    return crud.get_borrows_by_user(db, current_user.id)

@router.get("/", response_model=List[schemas.Borrow])
def get_all_borrows(
    db: Session = Depends(dependencies.get_db),
    current_admin: models.User = Depends(dependencies.get_current_admin)
):
    return crud.get_all_borrows(db) 