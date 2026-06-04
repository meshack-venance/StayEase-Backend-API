from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


DataT = TypeVar("DataT")


class APIResponse(BaseModel, Generic[DataT]):
    model_config = ConfigDict(populate_by_name=True)

    success: bool = Field(
        description="Shows whether the request completed successfully.",
        examples=[True],
    )
    message: str = Field(
        description="Human-readable result message.",
        examples=["Request completed successfully"],
    )
    data: DataT | None = Field(
        default=None,
        description="Response payload. It is omitted when there is no data.",
    )
    pagination: Any | None = Field(
        default=None,
        description="Pagination metadata for list endpoints.",
    )


def api_response(
    message: str,
    data: Any | None = None,
    success: bool = True,
    pagination: Any | None = None,
) -> APIResponse[Any]:
    return APIResponse(
        success=success,
        message=message,
        data=data,
        pagination=pagination,
    )
