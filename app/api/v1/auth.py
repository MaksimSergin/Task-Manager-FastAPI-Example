# app/api/v1/auth.py

from fastapi import APIRouter, HTTPException, status, Depends
from jose import jwt

from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token, TokenRefresh
from app.core.config import settings
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.services.user import get_user_by_username, create_user
from app.core.dependencies import redis_client

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """
    Register a new user.
    """
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")

    created_user = await create_user(user)
    if not created_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User creation failed.")
    return created_user

@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    """
    Authenticate a user and return access and refresh tokens.
    """
    db_user = await get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    access_token = create_access_token(data={"sub": str(db_user.id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id)})

    await redis_client.set(refresh_token, str(db_user.id), ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400)

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.post("/refresh", response_model=Token)
async def refresh_token(token_refresh: TokenRefresh):
    """
    Refresh the access token using a valid refresh token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token_refresh.refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    # Check if the refresh token exists in Redis
    stored_user_id = await redis_client.get(token_refresh.refresh_token)
    if stored_user_id is None or stored_user_id != user_id:
        raise credentials_exception

    access_token = create_access_token(data={"sub": user_id})
    new_refresh_token = create_refresh_token(data={"sub": user_id})

    await redis_client.set(new_refresh_token, user_id, ex=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400)
    await redis_client.delete(token_refresh.refresh_token)

    return Token(access_token=access_token, refresh_token=new_refresh_token, token_type="bearer")
