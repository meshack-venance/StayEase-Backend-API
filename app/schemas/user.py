from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.common import RecordStatus
from app.models.user import UserRole


class UserCreate(BaseModel):
    first_name: str = Field(
        min_length=2,
        max_length=100,
        description="Customer first name.",
        examples=["Meshack"],
    )
    last_name: str = Field(
        min_length=2,
        max_length=100,
        description="Customer last name.",
        examples=["Venance"],
    )
    email: EmailStr = Field(
        description="Unique email address used for login.",
        examples=["meshack@example.com"],
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Plain password sent during registration. The API stores only its hash.",
        examples=["password123"],
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique user id.", examples=[1])
    first_name: str = Field(description="User first name.", examples=["Meshack"])
    last_name: str = Field(description="User last name.", examples=["Venance"])
    email: EmailStr = Field(description="User email address.", examples=["meshack@example.com"])
    role: UserRole = Field(description="User role in the system.", examples=["CUSTOMER"])
    status: RecordStatus = Field(description="Current user account status.", examples=["ACTIVE"])
    created_at: datetime = Field(
        description="Date and time when the user account was created.",
        examples=["2026-06-03T12:00:00Z"],
    )
    updated_at: datetime = Field(
        description="Date and time when the user account was last updated.",
        examples=["2026-06-03T12:00:00Z"],
    )


class UserRegistrationResponse(BaseModel):
    success: Literal[True] = Field(
        default=True,
        description="Shows that the request completed successfully.",
    )
    message: Literal["User registered successfully"] = Field(
        default="User registered successfully",
        description="Human-readable result message.",
    )
    data: UserResponse = Field(description="The newly registered user.")


class CurrentUserResponse(BaseModel):
    success: Literal[True] = Field(
        default=True,
        description="Shows that the request completed successfully.",
    )
    message: Literal["Current user retrieved successfully"] = Field(
        default="Current user retrieved successfully",
        description="Human-readable result message.",
    )
    data: UserResponse = Field(description="The authenticated user.")


class UserListResponse(BaseModel):
    success: Literal[True] = Field(
        default=True,
        description="Shows that the request completed successfully.",
    )
    message: Literal["Users retrieved successfully"] = Field(
        default="Users retrieved successfully",
        description="Human-readable result message.",
    )
    data: list[UserResponse] = Field(description="All users visible to admins.")


class UserDetailResponse(BaseModel):
    success: Literal[True] = Field(
        default=True,
        description="Shows that the request completed successfully.",
    )
    message: Literal["User retrieved successfully"] = Field(
        default="User retrieved successfully",
        description="Human-readable result message.",
    )
    data: UserResponse = Field(description="The requested user.")
