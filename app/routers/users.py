from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.response import APIResponse, api_response
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=APIResponse[UserResponse],
    response_model_exclude_none=True,
)
def get_me(current_user: User = Depends(get_current_user)):
    return api_response(
        message="Current user retrieved successfully",
        data=current_user,
    )
