from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title=settings.app_name,
    description="Hotel Booking Backend API",
    version=settings.app_version,
    debug=settings.app_debug,
)


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
