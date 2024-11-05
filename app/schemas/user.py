# app/schemas/user.py

from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class UserInDB(UserOut):
    # Used only for internal database interactions
    password_hash: str
