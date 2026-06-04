from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.response import api_response
from app.schemas.upload import ProfileImageUploadResponse, PropertyImageUploadResponse
from app.services.property_service import get_property_by_id
from app.services.upload_service import save_image_upload

router = APIRouter(prefix="/api/v1/uploads", tags=["Uploads"])


@router.post(
    "/profile",
    response_model=ProfileImageUploadResponse,
    response_model_exclude_none=True,
    summary="Upload profile image",
    description="This endpoint is used by an authenticated user to upload or replace their profile image.",
    response_description="The uploaded profile image URL wrapped in the standard API response.",
)
async def upload_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    url = await save_image_upload(
        file,
        folder="profiles",
        filename_prefix=f"user-{current_user.id}",
    )
    current_user.profile_image_url = url
    db.commit()

    return api_response(
        message="Profile image uploaded successfully",
        data={"url": url},
    )


@router.post(
    "/properties/{property_id}",
    response_model=PropertyImageUploadResponse,
    response_model_exclude_none=True,
    summary="Upload property image",
    description="This endpoint is used by an authenticated user to upload or replace a property image.",
    response_description="The uploaded property image URL wrapped in the standard API response.",
)
async def upload_property_image(
    property_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    # Phase 7 checks authentication only; admin-only authorization comes in Phase 8.
    property_item = get_property_by_id(db, property_id)
    url = await save_image_upload(
        file,
        folder="properties",
        filename_prefix=f"property-{property_id}",
    )
    property_item.image_url = url
    db.commit()

    return api_response(
        message="Property image uploaded successfully",
        data={"url": url},
    )
