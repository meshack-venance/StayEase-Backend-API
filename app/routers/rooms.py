from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import require_admin
from app.dependencies.pagination import get_pagination_params
from app.models.user import User
from app.schemas.pagination import PaginationParams
from app.schemas.response import api_response
from app.schemas.room import (
    PropertyRoomListResponse,
    RoomCreate,
    RoomCreateResponse,
    RoomDeleteResponse,
    RoomDetailResponse,
    RoomListResponse,
    RoomUpdate,
    RoomUpdateResponse,
)
from app.services.room_service import (
    create_room,
    delete_room,
    get_room_by_id,
    get_rooms,
    get_rooms_by_property_id,
    update_room,
)

router = APIRouter(prefix="/api/v1/rooms", tags=["Rooms"])
property_rooms_router = APIRouter(prefix="/api/v1/properties", tags=["Rooms"])


@router.get(
    "",
    response_model=RoomListResponse,
    response_model_exclude_none=True,
    summary="List rooms",
    description="This endpoint is used to fetch active rooms with pagination and filters.",
    response_description="A list of rooms wrapped in the standard API response.",
)
def list_rooms(
    property_id: Annotated[
        int | None,
        Query(description="Filter rooms by property id."),
    ] = None,
    room_type: Annotated[
        str | None,
        Query(description="Filter rooms by type."),
    ] = None,
    min_price: Annotated[
        Decimal | None,
        Query(gt=0, description="Minimum nightly price."),
    ] = None,
    max_price: Annotated[
        Decimal | None,
        Query(gt=0, description="Maximum nightly price."),
    ] = None,
    capacity: Annotated[
        int | None,
        Query(ge=1, description="Minimum guest capacity."),
    ] = None,
    availability: Annotated[
        bool | None,
        Query(description="Filter by booking availability."),
    ] = None,
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
):
    rooms, total = get_rooms(
        db,
        pagination=pagination,
        property_id=property_id,
        room_type=room_type,
        min_price=min_price,
        max_price=max_price,
        capacity=capacity,
        availability=availability,
    )
    return api_response(
        message="Rooms retrieved successfully",
        data=rooms,
        pagination=pagination.to_meta(total),
    )


@property_rooms_router.get(
    "/{property_id}/rooms",
    response_model=PropertyRoomListResponse,
    response_model_exclude_none=True,
    summary="List rooms for a property",
    description="This endpoint is used to fetch all active rooms that belong to one property.",
    response_description="A list of property rooms wrapped in the standard API response.",
)
def list_property_rooms(property_id: int, db: Session = Depends(get_db)):
    rooms = get_rooms_by_property_id(db, property_id)
    return api_response(
        message="Property rooms retrieved successfully",
        data=rooms,
    )


@router.get(
    "/{room_id}",
    response_model=RoomDetailResponse,
    response_model_exclude_none=True,
    summary="Get room details",
    description="This endpoint is used to fetch one active room by its id.",
    response_description="The requested room wrapped in the standard API response.",
)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = get_room_by_id(db, room_id)
    return api_response(
        message="Room retrieved successfully",
        data=room,
    )


@router.post(
    "",
    response_model=RoomCreateResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create room",
    description="This endpoint is used by an admin to create a room under an existing property.",
    response_description="The newly created room wrapped in the standard API response.",
)
def create_new_room(
    room_data: RoomCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    # Only admins can manage rooms because rooms are part of platform inventory.
    room = create_room(db, room_data)
    return api_response(
        message="Room created successfully",
        data=room,
    )


@router.put(
    "/{room_id}",
    response_model=RoomUpdateResponse,
    response_model_exclude_none=True,
    summary="Update room",
    description="This endpoint is used by an admin to update an existing room.",
    response_description="The updated room wrapped in the standard API response.",
)
def update_existing_room(
    room_id: int,
    room_data: RoomUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    # Only admins can manage rooms because rooms are part of platform inventory.
    room = update_room(db, room_id, room_data)
    return api_response(
        message="Room updated successfully",
        data=room,
    )


@router.delete(
    "/{room_id}",
    response_model=RoomDeleteResponse,
    response_model_exclude_none=True,
    summary="Delete room",
    description="This endpoint is used by an admin to deactivate a room.",
    response_description="A success message wrapped in the standard API response.",
)
def delete_existing_room(
    room_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_admin),
):
    # Rooms are soft-deleted so booking history can stay connected later.
    delete_room(db, room_id)
    return api_response(message="Room deleted successfully")
