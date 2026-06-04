from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import require_admin
from app.dependencies.pagination import get_pagination_params
from app.models.common import RecordStatus
from app.models.user import User
from app.schemas.pagination import PaginationParams
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
    description="This endpoint is used to fetch accommodation properties with pagination, search, and filters.",
    response_description="A list of properties wrapped in the standard API response.",
)
def list_properties(
    search: Annotated[
        str | None,
        Query(description="Search by property name or description."),
    ] = None,
    location: Annotated[
        str | None,
        Query(description="Filter by property location."),
    ] = None,
    status_filter: Annotated[
        RecordStatus,
        Query(alias="status", description="Filter by property record status."),
    ] = RecordStatus.ACTIVE,
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
):
    properties, total = get_properties(
        db,
        pagination=pagination,
        search=search,
        location=location,
        status=status_filter,
    )
    return api_response(
        message="Properties retrieved successfully",
        data=properties,
        pagination=pagination.to_meta(total),
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
    description="This endpoint is used by an admin to create a new accommodation property.",
    response_description="The newly created property wrapped in the standard API response.",
)
def create_new_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    # Only admins can manage platform property records.
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
    description="This endpoint is used by an admin to update an existing accommodation property.",
    response_description="The updated property wrapped in the standard API response.",
)
def update_existing_property(
    property_id: int,
    property_data: PropertyUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    # Only admins can manage platform property records.
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
    description="This endpoint is used by an admin to delete an accommodation property.",
    response_description="A success message wrapped in the standard API response.",
)
def delete_existing_property(
    property_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    # Only admins can manage platform property records.
    delete_property(db, property_id)
    return api_response(message="Property deleted successfully")
