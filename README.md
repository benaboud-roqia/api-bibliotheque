# 📚 API Backend de Gestion de Bibliothèque

Une API REST sécurisée pour gérer une bibliothèque de livres, développée avec **FastAPI**, **SQLite** et **JWT**.

## 🚀 Fonctionnalités

- CRUD complet sur les livres (ajout, lecture, modification, suppression)
- Filtrage par auteur, titre, mot-clé, pagination
- Authentification sécurisée par JWT
- Gestion des utilisateurs (inscription, connexion, profil, rôles admin/user)
- Gestion des emprunts de livres (prêt/retour, historique)
- Commentaires et notes sur les livres
- Upload d'image de couverture pour les livres
- Export CSV de la liste des livres
- Gestion des erreurs standardisée (401, 403, 404, etc.)
- Documentation interactive (Swagger UI & Redoc)
- Tests unitaires avec Pytest

## 🛠️ Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/<ton-utilisateur>/<nom-du-repo>.git
   cd <nom-du-repo>
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Créer la base de données**
   ```bash
   python create_tables.py
   ```

4. **Lancer le serveur**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

5. **Accéder à la documentation**
   - Swagger UI : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🧪 Lancer les tests

```bash
python -m pytest
```

## 🔒 Authentification

- Inscris-toi via `/users/register`
- Connecte-toi via `/users/login` pour obtenir un token JWT
- Clique sur "Authorize" dans Swagger UI et colle le token :  
  `Bearer <ton_access_token>`

## 📦 Structure du projet

```
app/
  ├── main.py
  ├── models.py
  ├── schemas.py
  ├── database.py
  ├── crud.py
  ├── auth.py
  ├── dependencies.py
  ├── routers/
  │     ├── users.py
  │     ├── books.py
  │     ├── borrows.py
  │     └── reviews.py
  └── tests/
        ├── test_users.py
        └── test_books.py
create_tables.py
requirements.txt
README.md
```

## ✨ Fonctionnalités avancées

### 1. Commentaires et notes sur les livres
- Ajouter un commentaire/note : `POST /reviews/`
- Voir les commentaires d'un livre : `GET /reviews/book/{book_id}`
- Modifier/supprimer son commentaire : `PUT`/`DELETE /reviews/{review_id}`

### 2. Upload d'image de couverture
- Uploader une image : `POST /books/{book_id}/cover` (champ `file`)
- Le chemin de l'image est stocké dans `cover_url` du livre

### 3. Export CSV des livres
- Télécharger la liste des livres : `GET /books/export/csv`
- Fichier CSV prêt à être ouvert dans Excel ou Google Sheets

### 4. Emprunt de livres
- Emprunter un livre : `POST /borrows/`
- Rendre un livre : `POST /borrows/{borrow_id}/return`
- Voir ses emprunts : `GET /borrows/me`
- Voir tous les emprunts (admin) : `GET /borrows/`

### 5. Gestion des rôles
- Les routes sensibles sont réservées aux admins ou aux propriétaires
- Un admin peut voir tous les utilisateurs (`GET /users/`)

## 🧑‍💻 Exemples d'utilisation via Swagger UI

### a) Créer un utilisateur
```json
{
  "username": "monuser",
  "email": "monuser@email.com",
  "password": "motdepasse",
  "role": "admin"
}
```

### b) Se connecter et obtenir un token JWT
- Utilise `/users/login` avec tes identifiants
- Récupère le champ `access_token` dans la réponse

### c) Uploader une image de couverture
- Utilise `/books/{book_id}/cover` avec un fichier image (champ `file`)

### d) Exporter les livres en CSV
- Va sur `/books/export/csv` et télécharge le fichier

## 📝 Licence

Ce projet est open-source, libre à toi de l'adapter ! 
 ![image](https://github.com/user-attachments/assets/1b4304f0-d7ac-44f5-91fa-3910f5bb77e1)
