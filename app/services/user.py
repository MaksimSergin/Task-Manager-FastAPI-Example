# app/services/user.py

from typing import Optional
from asyncpg.exceptions import UniqueViolationError

from app.core.security import get_password_hash
from app.db.session import db
from app.schemas.user import UserCreate, UserOut, UserInDB


async def get_user_by_username(username: str) -> Optional[UserInDB]:
    """
    Retrieve a user by username, including password_hash for authentication.
    """
    query = "SELECT id, username, password_hash FROM users WHERE username = $1"
    record = await db.fetchrow(query, username)
    return UserInDB(**record) if record else None

async def create_user(user: UserCreate) -> Optional[UserOut]:
    """
    Creates a new user with a hashed password.
    """
    hashed_password = get_password_hash(user.password)

    query = """
    INSERT INTO users (username, password_hash)
    VALUES ($1, $2)
    RETURNING id, username
    """
    try:
        record = await db.fetchrow(query, user.username, hashed_password)
        return UserOut(**record) if record else None
    except UniqueViolationError:
        return None
