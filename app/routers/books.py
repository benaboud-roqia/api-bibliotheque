from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, models, crud, dependencies
import shutil
import os
from fastapi.responses import StreamingResponse
import csv
from io import StringIO

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 10,
    author: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(dependencies.get_db)
):
    return crud.get_books(db, skip=skip, limit=limit, author=author, title=title, keyword=keyword)

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(dependencies.get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    return crud.create_book(db, book, user_id=current_user.id)

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this book")
    return crud.update_book(db, db_book, book_update)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this book")
    crud.delete_book(db, db_book)
    return None

@router.post("/{book_id}/cover", response_model=schemas.Book)
def upload_cover(
    book_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this book")
    # Sauvegarde du fichier dans un dossier 'covers/'
    os.makedirs("covers", exist_ok=True)
    file_path = f"covers/book_{book_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    db_book.cover_url = file_path
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/export/csv")
def export_books_csv(db: Session = Depends(dependencies.get_db)):
    books = crud.get_books(db, skip=0, limit=10000)
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "title", "author", "description", "cover_url", "owner_id"])
    for book in books:
        writer.writerow([
            book.id,
            book.title,
            book.author,
            book.description or "",
            book.cover_url or "",
            book.owner_id
        ])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=books.csv"}) 