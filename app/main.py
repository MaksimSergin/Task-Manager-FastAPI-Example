# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import auth, tasks
from app.db.session import db, init_models
import uvicorn

def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await db.connect()
        await init_models()
        yield
        await db.disconnect()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="A robust task management API with authentication.",
        version="1.0.0",
        lifespan=lifespan
    )

    cors_origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else settings.CORS_ORIGINS.split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])

    @app.get("/health", tags=["Health Check"])
    async def health_check():
        return {"status": "ok"}

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
