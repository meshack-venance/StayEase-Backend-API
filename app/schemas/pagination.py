from math import ceil

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(description="Current page number.")
    size: int = Field(description="Number of records per page.")

    @property
    def offset(self) -> int:
        # SQL OFFSET is zero-based, while API page numbers are easier to read from 1.
        return (self.page - 1) * self.size

    def to_meta(self, total: int) -> "PaginationMeta":
        pages = ceil(total / self.size) if total else 0
        return PaginationMeta(
            page=self.page,
            size=self.size,
            total=total,
            pages=pages,
        )


class PaginationMeta(BaseModel):
    page: int = Field(description="Current page number.", examples=[1])
    size: int = Field(description="Number of records per page.", examples=[10])
    total: int = Field(description="Total number of records matching the query.", examples=[25])
    pages: int = Field(description="Total number of available pages.", examples=[3])
