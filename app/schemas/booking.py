from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.booking import BookingStatus


class BookingCreate(BaseModel):
    room_id: int = Field(
        description="Room id the customer wants to book.",
        examples=[1],
    )
    check_in: date = Field(
        description="First date of the stay.",
        examples=["2026-06-10"],
    )
    check_out: date = Field(
        description="Checkout date. Must be after check-in.",
        examples=["2026-06-15"],
    )


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique booking id.", examples=[1])
    user_id: int = Field(description="Customer user id.", examples=[1])
    room_id: int = Field(description="Booked room id.", examples=[1])
    check_in: date = Field(description="First date of the stay.")
    check_out: date = Field(description="Checkout date.")
    status: BookingStatus = Field(description="Current booking status.")
    created_at: datetime = Field(description="Date and time when the booking was created.")
    updated_at: datetime = Field(description="Date and time when the booking was last updated.")


class BookingCreateResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Booking created successfully"] = "Booking created successfully"
    data: BookingResponse


class MyBookingListResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Bookings retrieved successfully"] = "Bookings retrieved successfully"
    data: list[BookingResponse]


class BookingCancelResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Booking cancelled successfully"] = "Booking cancelled successfully"
    data: BookingResponse
