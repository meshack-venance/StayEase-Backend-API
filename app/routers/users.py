from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.response import api_response
from app.schemas.user import CurrentUserResponse

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


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
