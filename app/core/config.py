# app/core/config.py

from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Manager API"
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = Field(..., env="CORS_ORIGINS")

    @classmethod
    def _assemble_cors_origins(cls, cors_origins: Union[str, List[AnyHttpUrl]]) -> List[AnyHttpUrl]:
        if isinstance(cors_origins, str):
            return [origin.strip() for origin in cors_origins.split(",")]
        return cors_origins

    class Config:
        env_file = ".env"

settings = Settings()
