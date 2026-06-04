from typing import Annotated

from fastapi import Query

from app.schemas.pagination import PaginationParams


def get_pagination_params(
    page: Annotated[int, Query(ge=1, description="Page number, starting from 1.")] = 1,
    size: Annotated[int, Query(ge=1, le=100, description="Number of records per page.")] = 10,
) -> PaginationParams:
    # This dependency is the FastAPI version of a small Spring Pageable resolver.
    return PaginationParams(page=page, size=size)
