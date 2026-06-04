from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        description="Email address used during registration.",
        examples=["meshack@example.com"],
    )
    password: str = Field(
        min_length=1,
        description="User password.",
        examples=["password123"],
    )


class TokenResponse(BaseModel):
    access_token: str = Field(
        description="JWT access token used to call protected endpoints.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        default="bearer",
        description="Authentication scheme for the access token.",
        examples=["bearer"],
    )


class LoginResponse(BaseModel):
    success: Literal[True] = Field(
        default=True,
        description="Shows that the request completed successfully.",
    )
    message: Literal["Login successful"] = Field(
        default="Login successful",
        description="Human-readable result message.",
    )
    data: TokenResponse = Field(description="JWT token details.")
