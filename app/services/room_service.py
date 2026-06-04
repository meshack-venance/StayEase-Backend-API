from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import StayEaseException
from app.models.common import RecordStatus
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate
from app.services.property_service import get_property_by_id


def get_rooms(db: Session) -> list[Room]:
    statement = (
        select(Room)
        .where(Room.status == RecordStatus.ACTIVE)
        .order_by(Room.created_at.desc())
    )
    return list(db.scalars(statement))


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
