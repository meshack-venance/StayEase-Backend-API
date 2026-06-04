from typing import Literal

from pydantic import BaseModel, Field


class UploadResponseData(BaseModel):
    url: str = Field(
        description="Public URL path for the uploaded file.",
        examples=["/uploads/profiles/user-1-a1b2c3.png"],
    )


class ProfileImageUploadResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Profile image uploaded successfully"] = "Profile image uploaded successfully"
    data: UploadResponseData


class PropertyImageUploadResponse(BaseModel):
    success: Literal[True] = True
    message: Literal["Property image uploaded successfully"] = "Property image uploaded successfully"
    data: UploadResponseData
