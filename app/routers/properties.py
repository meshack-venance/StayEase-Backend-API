from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.property import (
    PropertyCreate,
    PropertyCreateResponse,
    PropertyDeleteResponse,
    PropertyDetailResponse,
    PropertyListResponse,
    PropertyUpdate,
    PropertyUpdateResponse,
)
from app.schemas.response import api_response
from app.services.property_service import (
    create_property,
    delete_property,
    get_properties,
    get_property_by_id,
    update_property,
)

router = APIRouter(prefix="/api/v1/properties", tags=["Properties"])


@router.get(
    "",
    response_model=PropertyListResponse,
    response_model_exclude_none=True,
    summary="List properties",
    description="This endpoint is used to fetch all accommodation properties that customers can browse.",
    response_description="A list of properties wrapped in the standard API response.",
)
def list_properties(db: Session = Depends(get_db)):
    properties = get_properties(db)
    return api_response(
        message="Properties retrieved successfully",
        data=properties,
    )


@router.get(
    "/{property_id}",
    response_model=PropertyDetailResponse,
    response_model_exclude_none=True,
    summary="Get property details",
    description="This endpoint is used to fetch one accommodation property by its id.",
    response_description="The requested property wrapped in the standard API response.",
)
def get_property(property_id: int, db: Session = Depends(get_db)):
    property_item = get_property_by_id(db, property_id)
    return api_response(
        message="Property retrieved successfully",
        data=property_item,
    )


@router.post(
    "",
    response_model=PropertyCreateResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create property",
    description="This endpoint is used to create a new accommodation property. The user must be authenticated.",
    response_description="The newly created property wrapped in the standard API response.",
)
def create_new_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    # Phase 4 only checks authentication; admin-only authorization comes in Phase 8.
    property_item = create_property(db, property_data)
    return api_response(
        message="Property created successfully",
        data=property_item,
    )


@router.put(
    "/{property_id}",
    response_model=PropertyUpdateResponse,
    response_model_exclude_none=True,
    summary="Update property",
    description="This endpoint is used to update an existing accommodation property. The user must be authenticated.",
    response_description="The updated property wrapped in the standard API response.",
)
def update_existing_property(
    property_id: int,
    property_data: PropertyUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    # Phase 4 only checks authentication; admin-only authorization comes in Phase 8.
    property_item = update_property(db, property_id, property_data)
    return api_response(
        message="Property updated successfully",
        data=property_item,
    )


@router.delete(
    "/{property_id}",
    response_model=PropertyDeleteResponse,
    response_model_exclude_none=True,
    summary="Delete property",
    description="This endpoint is used to delete an accommodation property. The user must be authenticated.",
    response_description="A success message wrapped in the standard API response.",
)
def delete_existing_property(
    property_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    # Phase 4 only checks authentication; admin-only authorization comes in Phase 8.
    delete_property(db, property_id)
    return api_response(message="Property deleted successfully")
