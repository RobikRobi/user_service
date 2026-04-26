import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from users_service.app.shemas import CreateUser
from users_service.app.db import get_connection, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="User service", lifespan=lifespan)


@app.get("/status")
async def status_service() -> dict[str, str]:
    return {"status": "ok", "service": "user_service"}

@app.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUser) -> dict[str, int | str]:
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
                """,
                (data.username, data.email, data.password),
            )
            connection.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists",
        )

    return {
        "id": cursor.lastrowid,
        "username": data.username,
        "email": data.email,
    }


@app.get("/users")
async def all_users() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute("SELECT id, username, email " \
        "FROM users " \
        "ORDER BY id").fetchall()
        return [dict(row) for row in rows]

@app.get("/users/{user_id}")
async def get_user(user_id: int) -> dict:
    with get_connection() as connection:
        user = connection.execute("SELECT id, username, email \
                                  FROM users \
                                  WHERE id=?", 
                                  (user_id,)).fetchone()
        if user is None:
            raise HTTPException(status_code=404, 
                                detail=f"User {user_id} not found")
    return dict(user)

