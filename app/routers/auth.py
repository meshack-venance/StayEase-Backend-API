from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import StayEaseException
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import authenticate_user, create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user is not None:
        raise StayEaseException(
            message="Email is already registered",
            status_code=status.HTTP_409_CONFLICT,
        )

    return create_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if user is None:
        raise StayEaseException(
            message="Invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)
