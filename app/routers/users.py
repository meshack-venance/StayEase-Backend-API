from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import StayEaseException
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User
from app.schemas.response import api_response
from app.schemas.user import CurrentUserResponse, UserDetailResponse, UserListResponse
from app.services.user_service import get_user_by_id, get_users

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get(
    "",
    response_model=UserListResponse,
    response_model_exclude_none=True,
    summary="List users",
    description="This endpoint is used by an admin to view all users in the system.",
    response_description="All users wrapped in the standard API response.",
)
def list_users(
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    # Admin route: useful for support, audits, and future user-management features.
    users = get_users(db)
    return api_response(
        message="Users retrieved successfully",
        data=users,
    )


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    response_model_exclude_none=True,
    summary="Get current user",
    description="This endpoint is used to retrieve the profile of the currently authenticated user. The request must include a valid bearer token.",
    response_description="The authenticated user wrapped in the standard API response.",
)
def get_me(current_user: User = Depends(get_current_user)):
    return api_response(
        message="Current user retrieved successfully",
        data=current_user,
    )


@router.get(
    "/{user_id}",
    response_model=UserDetailResponse,
    response_model_exclude_none=True,
    summary="Get user details",
    description="This endpoint is used by an admin to view one user by id.",
    response_description="The requested user wrapped in the standard API response.",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise StayEaseException("User not found", status_code=404)

    return api_response(
        message="User retrieved successfully",
        data=user,
    )
