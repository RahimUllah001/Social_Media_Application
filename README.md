# Social_Media_Application
# Social Media Application using FastAPI, SQLAlchemy, Alembic, and PostgreSQL

## Table of Contents
1. [Overview](#overview)
2. [Technologies Used](#technologies-used)
3. [Features](#features)
4. [Folder Structure](#folder-structure)
5. [Setup Instructions](#setup-instructions)
6. [Core Functionalities](#core-functionalities)
7. [Database Models](#database-models)
8. [API Endpoints](#api-endpoints)
9. [Authentication & JWT Tokens](#authentication--jwt-tokens)
10. [CORS Middleware](#cors-middleware)
11. [Migration using Alembic](#migration-using-alembic)
12. [How to Contribute](#how-to-contribute)
13. [Conclusion](#conclusion)

---

## Overview
This is a social media backend application built with **FastAPI** and **PostgreSQL**, using **SQLAlchemy** for ORM and **Alembic** for database migrations. The application allows users to perform core social media operations such as:

- User registration and login
- Follow and unfollow users
- Create, update, delete, and read posts (with optional image uploads)
- Like and unlike posts
- Password reset functionality

Authentication is implemented using **JWT tokens** to ensure secure user interactions.

---

## Technologies Used
- **FastAPI**: Web framework for building APIs
- **PostgreSQL**: Database for persistent storage
- **SQLAlchemy**: ORM for database interaction
- **Alembic**: Database migration tool
- **JWT Tokens**: Authentication mechanism
- **Pydantic**: Data validation and parsing
- **CORS Middleware**: Allows cross-origin requests

---

## Features
1. **User Management**:
   - User registration
   - Login and logout
   - Password reset (with token)
   - Deleting a user account

2. **Follow System**:
   - Follow and unfollow users
   - Track followers and following counts

3. **Posts**:
   - Create, update, and delete posts
   - Read all or specific posts
   - Optionally upload images with descriptions

4. **Likes**:
   - Like and unlike a post
   - Track post likes

5. **Authentication**:
   - JWT token-based authentication for secure API endpoints

6. **Middleware**:
   - CORS middleware to allow frontend access

---

## Folder Structure
```
project/
│-- alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
│-- routers/
│   ├── auth.py
│   ├── post.py
│   ├── user.py
│   ├── like.py
│   └── __init__.py
│
│-- static/
│   ├── __init__.py
│   ├── .env
│
│-- .gitignore
│-- alembic.ini
│-- config.py
│-- database.py
│-- explanation.txt
│-- fadapi_app.sql
│-- main.py
│-- models.py
│-- oauth2.py
│-- schemas.py
│-- tut.txt
│-- utils.py
```
---

## Setup Instructions
Follow these steps to set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd project
   ```



2. **Set up PostgreSQL database**:
   - Create a PostgreSQL database (e.g., `social_media_db`).
   - Update the database connection details in `config.py`.

3. **Run Alembic migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Test the API**:
   - Open `http://127.0.0.1:8000/docs` to access the Swagger UI.

---

## Core Functionalities

### 1. **User Management**
- **Register**: Create a new user account.
- **Login**: Authenticate user credentials and issue JWT tokens.
- **Reset Password**: Generate a reset token for password recovery.

### 2. **Follow System**
- Follow and unfollow users.
- Track the number of followers and followings.

### 3. **Posts**
- Users can create posts with or without an image.
- Posts can be updated or deleted.
- Retrieve all posts or specific posts by ID.

### 4. **Likes**
- Users can like or unlike posts.
- View total likes for a post.

### 5. **Authentication**
- JWT tokens are used to secure endpoints and authenticate users.

---

## Database Models

### User Model
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)
```

### Post Model
```python
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")
```

### Follow Model
```python
class Follow(Base):
    __tablename__ = 'follows'
    id = Column(Integer, primary_key=True, nullable=False)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    followee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
```

### Like Model
```python
class Like(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
```

---

## API Endpoints
Here are the main endpoints:

| Method | Endpoint             | Description                |
|--------|----------------------|----------------------------|
| POST   | `/users`             | Create a new user          |
| POST   | `/login`             | Authenticate a user        |
| POST   | `/follow`            | Follow a user              |
| POST   | `/unfollow`          | Unfollow a user            |
| POST   | `/posts`             | Create a post              |
| GET    | `/posts`             | Get all posts              |
| PUT    | `/posts/{id}`        | Update a specific post     |
| DELETE | `/posts/{id}`        | Delete a specific post     |
| POST   | `/like`              | Like a post                |
| POST   | `/forget-password`    | Request password reset     |

---

## Authentication & JWT Tokens
JWT-based authentication ensures secure API communication. Use the `Authorization` header to send the bearer token.

Example:
```
Authorization: Bearer <token>
```

---

## CORS Middleware
To allow frontend access to the backend:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Migration using Alembic
To apply database migrations:
```bash
alembic revision --autogenerate -m "create tables"
alembic upgrade head
```

---

## How to Contribute
1. Fork the repository.
2. Clone the repository locally.
3. Create a new branch for your feature.
4. Commit your changes and submit a PR.

---

## Conclusion
This social media application serves as a solid foundation for building a robust backend with FastAPI and PostgreSQL. It is designed to be extensible and secure, enabling further customization as needed.
