from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base, engine, get_db
from app.models import user
from app.routers import auth, users


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        # Learning shortcut: create tables on startup. Real projects usually use Alembic migrations.
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as exc:
        print(f"Database initialization skipped: {exc}")
    yield

app = FastAPI(
    title=settings.app_name,
    description="Hotel Booking Backend API",
    version=settings.app_version,
    debug=settings.app_debug,
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to StayEase API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "running"
    }


@app.get("/health/database")
def database_health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is not reachable",
        ) from exc

    return {
        "database": "connected"
    }
