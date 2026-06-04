from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.common import RecordStatus


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String(255), index=True)
    # Numeric keeps ratings precise in PostgreSQL, unlike float which can introduce rounding noise.
    rating: Mapped[Decimal] = mapped_column(
        Numeric(precision=2, scale=1),
        default=Decimal("0.0"),
    )
    # Status lets us hide or deactivate records without deleting their history.
    status: Mapped[RecordStatus] = mapped_column(
        Enum(RecordStatus, name="record_status"),
        default=RecordStatus.ACTIVE,
    )
    # The database sets this value, so every inserted row gets a consistent timestamp.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    # updated_at changes whenever SQLAlchemy updates this row.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
