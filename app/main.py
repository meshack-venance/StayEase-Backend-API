from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import Depends, FastAPI, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base, engine, get_db
from app.core.exception_handlers import register_exception_handlers
from app.core.exceptions import StayEaseException
from app.models import property, user
from app.routers import auth, properties, users


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

register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(properties.router)
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
        raise StayEaseException(
            message="Database is not reachable",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        ) from exc

    return {
        "database": "connected"
    }
