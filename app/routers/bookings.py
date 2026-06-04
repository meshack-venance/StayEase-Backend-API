from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.booking import (
    BookingCancelResponse,
    BookingCreate,
    BookingCreateResponse,
    MyBookingListResponse,
)
from app.schemas.response import api_response
from app.services.booking_service import cancel_booking, create_booking, get_my_bookings

router = APIRouter(prefix="/api/v1/bookings", tags=["Bookings"])


@router.post(
    "",
    response_model=BookingCreateResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create booking",
    description="This endpoint is used by an authenticated customer to book an available room for a date range.",
    response_description="The newly created booking wrapped in the standard API response.",
)
def create_new_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = create_booking(db, booking_data, current_user)
    return api_response(
        message="Booking created successfully",
        data=booking,
    )


@router.get(
    "/my",
    response_model=MyBookingListResponse,
    response_model_exclude_none=True,
    summary="List my bookings",
    description="This endpoint is used by an authenticated customer to view their own bookings.",
    response_description="The customer's bookings wrapped in the standard API response.",
)
def list_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookings = get_my_bookings(db, current_user)
    return api_response(
        message="Bookings retrieved successfully",
        data=bookings,
    )


@router.delete(
    "/{booking_id}",
    response_model=BookingCancelResponse,
    response_model_exclude_none=True,
    summary="Cancel booking",
    description="This endpoint is used by an authenticated customer to cancel one of their own bookings.",
    response_description="The cancelled booking wrapped in the standard API response.",
)
def cancel_existing_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Ownership is checked in the service using current_user.id.
    booking = cancel_booking(db, booking_id, current_user)
    return api_response(
        message="Booking cancelled successfully",
        data=booking,
    )
