from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.common import RecordStatus


class RoomCreate(BaseModel):
    property_id: int = Field(
        description="Property id that owns this room.",
        examples=[1],
    )
    room_number: str = Field(
        min_length=1,
        max_length=50,
        description="Room number or label inside the property.",
        examples=["A-101"],
    )
    room_type: str = Field(
        min_length=2,
        max_length=100,
        description="Customer-facing room type.",
        examples=["Deluxe Double"],
    )
    price_per_night: Decimal = Field(
        gt=0,
        description="Nightly room price.",
        examples=["120.00"],
    )
    capacity: int = Field(
        ge=1,
        description="Maximum number of guests allowed in the room.",
        examples=[2],
    )
    availability: bool = Field(
        default=True,
        description="Shows whether the room can currently be booked.",
        examples=[True],
    )


class RoomUpdate(BaseModel):
    # Update fields are optional so clients can send only changed values.
    room_number: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Updated room number or label inside the property.",
        examples=["A-102"],
    )
    room_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="Updated customer-facing room type.",
        examples=["Executive Suite"],
    )
    price_per_night: Decimal | None = Field(
        default=None,
        gt=0,
        description="Updated nightly room price.",
        examples=["180.00"],
    )
    capacity: int | None = Field(
        default=None,
        ge=1,
        description="Updated maximum number of guests allowed in the room.",
        examples=[3],
    )
    availability: bool | None = Field(
        default=None,
        description="Updated room booking availability.",
        examples=[False],
    )


class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique room id.", examples=[1])
    property_id: int = Field(description="Property id that owns this room.", examples=[1])
    room_number: str = Field(description="Room number or label inside the property.")
    room_type: str = Field(description="Customer-facing room type.")
    price_per_night: Decimal = Field(description="Nightly room price.")
    capacity: int = Field(description="Maximum number of guests allowed in the room.")
    availability: bool = Field(description="Shows whether the room can currently be booked.")
    status: RecordStatus = Field(description="Current room record status.")
    created_at: datetime = Field(description="Date and time when the room was created.")
    updated_at: datetime = Field(description="Date and time when the room was last updated.")


class RoomCreateResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Room created successfully"] = "Room created successfully"
    data: RoomResponse


class RoomDetailResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Room retrieved successfully"] = "Room retrieved successfully"
    data: RoomResponse


class RoomListResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Rooms retrieved successfully"] = "Rooms retrieved successfully"
    data: list[RoomResponse]


class PropertyRoomListResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Property rooms retrieved successfully"] = "Property rooms retrieved successfully"
    data: list[RoomResponse]


class RoomUpdateResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Room updated successfully"] = "Room updated successfully"
    data: RoomResponse


class RoomDeleteResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Room deleted successfully"] = "Room deleted successfully"
