from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import StayEaseException
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, LoginResponse, TokenResponse
from app.schemas.response import api_response
from app.schemas.user import UserCreate, UserRegistrationResponse
from app.services.user_service import authenticate_user, create_user, get_user_by_email

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserRegistrationResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Register a customer account",
    description="This endpoint is used to create a new customer account. It validates the email, hashes the password, and stores the user in the database.",
    response_description="The newly registered user wrapped in the standard API response.",
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user is not None:
        raise StayEaseException(
            message="Email is already registered",
            status_code=status.HTTP_409_CONFLICT,
        )

    user = create_user(db, user_data)
    return api_response(
        message="User registered successfully",
        data=user,
    )


@router.post(
    "/login",
    response_model=LoginResponse,
    response_model_exclude_none=True,
    summary="Login a user",
    description="This endpoint is used to authenticate a registered user with email and password. If the credentials are valid, it returns a JWT access token.",
    response_description="A JWT access token wrapped in the standard API response.",
)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if user is None:
        raise StayEaseException(
            message="Invalid email or password",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(subject=str(user.id))
    return api_response(
        message="Login successful",
        data=TokenResponse(access_token=token),
    )
