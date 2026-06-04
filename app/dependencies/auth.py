from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import StayEaseException
from app.core.security import decode_access_token
from app.models.user import User, UserRole
from app.services.user_service import get_user_by_id


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    # Route guard: decode the bearer token, load the user, or reject the request.
    credentials_exception = StayEaseException(
        message="Could not validate credentials",
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = decode_access_token(token)
        user_id = payload.get("sub")
    except jwt.PyJWTError as exc:
        raise credentials_exception from exc

    if user_id is None:
        raise credentials_exception

    user = get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception

    return user


def require_admin(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    # Role guard: authenticate first, then allow only platform administrators.
    if current_user.role != UserRole.ADMIN:
        raise StayEaseException(
            message="Admin access is required",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return current_user


def require_customer(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    # Role guard: useful when a route should be limited to customer workflows.
    if current_user.role != UserRole.CUSTOMER:
        raise StayEaseException(
            message="Customer access is required",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return current_user
