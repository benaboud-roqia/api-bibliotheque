from fastapi import FastAPI
from app.routers import users, books
from app.routers import borrows, reviews
from app import models, database
import uvicorn

app = FastAPI(title="API Gestion Bibliothèque", description="API REST sécurisée pour la gestion d'une bibliothèque de livres.")

# Création des tables au démarrage
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

# Inclusion des routeurs
app.include_router(users.router)
app.include_router(books.router)
app.include_router(borrows.router)
app.include_router(reviews.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 