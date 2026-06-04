from pathlib import Path

from fastapi import Depends, FastAPI, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import StayEaseException
from app.core.exceptions.handlers import register_exception_handlers
from app.routers import auth, bookings, properties, rooms, uploads, users


app = FastAPI(
    title=settings.app_name,
    description="Hotel Booking Backend API",
    version=settings.app_version,
    debug=settings.app_debug,
)

register_exception_handlers(app)

# StaticFiles works like Spring Boot's static resources: files saved here can be
# requested later from the browser or API clients using their public URL.
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(rooms.router)
app.include_router(rooms.property_rooms_router)
app.include_router(bookings.router)
app.include_router(uploads.router)
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
