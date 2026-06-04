from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.common import RecordStatus
from app.schemas.pagination import PaginationMeta


class PropertyCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150,
        description="Public name of the accommodation property.",
        examples=["StayEase City Hotel"],
    )
    description: str = Field(
        min_length=10,
        description="Detailed description shown to customers.",
        examples=["Modern hotel near the city center with free Wi-Fi."],
    )
    location: str = Field(
        min_length=2,
        max_length=255,
        description="Human-readable property location.",
        examples=["Dar es Salaam, Tanzania"],
    )
    rating: Decimal = Field(
        default=Decimal("0.0"),
        ge=0,
        le=5,
        description="Property rating from 0.0 to 5.0.",
        examples=["4.5"],
    )


class PropertyUpdate(BaseModel):
    # Update fields are optional so clients can send only the values they want to change.
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
        description="Updated public name of the accommodation property.",
        examples=["StayEase City Hotel"],
    )
    description: str | None = Field(
        default=None,
        min_length=10,
        description="Updated detailed description shown to customers.",
        examples=["Modern hotel near the city center with free Wi-Fi and breakfast."],
    )
    location: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
        description="Updated human-readable property location.",
        examples=["Dar es Salaam, Tanzania"],
    )
    rating: Decimal | None = Field(
        default=None,
        ge=0,
        le=5,
        description="Updated property rating from 0.0 to 5.0.",
        examples=["4.7"],
    )


class PropertyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique property id.", examples=[1])
    name: str = Field(description="Public name of the accommodation property.")
    description: str = Field(description="Detailed description shown to customers.")
    location: str = Field(description="Human-readable property location.")
    rating: Decimal = Field(description="Property rating from 0.0 to 5.0.")
    status: RecordStatus = Field(description="Current property status.")
    created_at: datetime = Field(description="Date and time when the property was created.")
    updated_at: datetime = Field(description="Date and time when the property was last updated.")


class PropertyCreateResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Property created successfully"] = "Property created successfully"
    data: PropertyResponse


class PropertyDetailResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Property retrieved successfully"] = "Property retrieved successfully"
    data: PropertyResponse


class PropertyListResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Properties retrieved successfully"] = "Properties retrieved successfully"
    data: list[PropertyResponse]
    pagination: PaginationMeta


class PropertyUpdateResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Property updated successfully"] = "Property updated successfully"
    data: PropertyResponse


class PropertyDeleteResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Property deleted successfully"] = "Property deleted successfully"
