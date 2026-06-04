from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.common import RecordStatus


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (
        # A room number should be unique inside one property, but can repeat across properties.
        UniqueConstraint("property_id", "room_number", name="uq_rooms_property_room_number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # ForeignKey creates the many-to-one link: many rooms belong to one property.
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), index=True)
    room_number: Mapped[str] = mapped_column(String(50))
    room_type: Mapped[str] = mapped_column(String(100), index=True)
    price_per_night: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    capacity: Mapped[int] = mapped_column(Integer)
    availability: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[RecordStatus] = mapped_column(
        Enum(RecordStatus, name="record_status"),
        default=RecordStatus.ACTIVE,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    property: Mapped["Property"] = relationship(back_populates="rooms")
