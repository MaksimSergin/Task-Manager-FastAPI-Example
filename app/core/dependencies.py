# app/core/dependencies.py
import redis.asyncio as redis
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.db.session import db
from app.schemas.token import TokenData
from app.schemas.user import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    """
    Retrieves the current authenticated user based on the JWT access token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id))
    except (JWTError, ValueError):
        raise credentials_exception

    query = "SELECT * FROM users WHERE id = $1"
    user_record = await db.fetchrow(query, token_data.user_id)
    if user_record is None:
        raise credentials_exception
    user = UserOut(**user_record)
    return user
