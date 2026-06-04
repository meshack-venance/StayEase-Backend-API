from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import StayEaseException
from app.models.common import RecordStatus
from app.models.room import Room
from app.schemas.pagination import PaginationParams
from app.schemas.room import RoomCreate, RoomUpdate
from app.services.property_service import get_property_by_id


def get_rooms(
    db: Session,
    pagination: PaginationParams,
    property_id: int | None = None,
    room_type: str | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    capacity: int | None = None,
    availability: bool | None = None,
) -> tuple[list[Room], int]:
    if min_price is not None and max_price is not None and max_price < min_price:
        raise StayEaseException(
            "max_price must be greater than or equal to min_price",
            status_code=400,
        )

    filters = [Room.status == RecordStatus.ACTIVE]

    if property_id is not None:
        get_property_by_id(db, property_id)
        filters.append(Room.property_id == property_id)

    if room_type:
        filters.append(Room.room_type.ilike(f"%{room_type}%"))

    if min_price is not None:
        filters.append(Room.price_per_night >= min_price)

    if max_price is not None:
        filters.append(Room.price_per_night <= max_price)

    if capacity is not None:
        filters.append(Room.capacity >= capacity)

    if availability is not None:
        filters.append(Room.availability == availability)

    count_statement = select(func.count()).select_from(Room).where(*filters)
    statement = (
        select(Room)
        .where(*filters)
        .order_by(Room.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.size)
    )
    return list(db.scalars(statement)), db.scalar(count_statement) or 0


def get_rooms_by_property_id(db: Session, property_id: int) -> list[Room]:
    # Validate the parent property first so unknown properties return a clear 404.
    get_property_by_id(db, property_id)
    statement = (
        select(Room)
        .where(
            Room.property_id == property_id,
            Room.status == RecordStatus.ACTIVE,
        )
        .order_by(Room.room_number)
    )
    return list(db.scalars(statement))


def get_room_by_id(db: Session, room_id: int) -> Room:
    statement = select(Room).where(
        Room.id == room_id,
        Room.status == RecordStatus.ACTIVE,
    )
    room = db.scalar(statement)
    if room is None:
        raise StayEaseException("Room not found", status_code=404)
    return room


def create_room(db: Session, room_data: RoomCreate) -> Room:
    get_property_by_id(db, room_data.property_id)
    _ensure_room_number_is_available(
        db,
        property_id=room_data.property_id,
        room_number=room_data.room_number,
    )

    room = Room(**room_data.model_dump())
    db.add(room)
    db.commit()
    # Refresh loads database-generated values such as id and timestamps.
    db.refresh(room)
    return room


def update_room(db: Session, room_id: int, room_data: RoomUpdate) -> Room:
    room = get_room_by_id(db, room_id)
    update_data = room_data.model_dump(exclude_unset=True)

    if "room_number" in update_data:
        _ensure_room_number_is_available(
            db,
            property_id=room.property_id,
            room_number=update_data["room_number"],
            current_room_id=room.id,
        )

    # exclude_unset keeps omitted fields unchanged during partial updates.
    for field, value in update_data.items():
        setattr(room, field, value)

    db.commit()
    db.refresh(room)
    return room


def delete_room(db: Session, room_id: int) -> None:
    room = get_room_by_id(db, room_id)
    # Soft delete keeps historical references while hiding the room from normal reads.
    room.status = RecordStatus.INACTIVE
    db.commit()


def _ensure_room_number_is_available(
    db: Session,
    property_id: int,
    room_number: str,
    current_room_id: int | None = None,
) -> None:
    statement = select(Room).where(
        Room.property_id == property_id,
        Room.room_number == room_number,
    )
    existing_room = db.scalar(statement)
    if existing_room is None:
        return
    if current_room_id is not None and existing_room.id == current_room_id:
        return

    raise StayEaseException(
        "Room number already exists for this property",
        status_code=409,
    )
