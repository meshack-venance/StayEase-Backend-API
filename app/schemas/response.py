from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


DataT = TypeVar("DataT")


class APIResponse(BaseModel, Generic[DataT]):
    model_config = ConfigDict(populate_by_name=True)

    has_error: bool = Field(alias="hasError")
    message: str
    data: DataT | None = None
    pagination: Any | None = None


def api_response(
    message: str,
    data: Any | None = None,
    has_error: bool = False,
    pagination: Any | None = None,
) -> APIResponse[Any]:
    return APIResponse(
        has_error=has_error,
        message=message,
        data=data,
        pagination=pagination,
    )
