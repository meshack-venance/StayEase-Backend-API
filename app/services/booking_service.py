from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import StayEaseException
from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.schemas.booking import BookingCreate
from app.schemas.pagination import PaginationParams
from app.services.room_service import get_room_by_id


def create_booking(
    db: Session,
    booking_data: BookingCreate,
    current_user: User,
) -> Booking:
    _validate_booking_dates(booking_data.check_in, booking_data.check_out)

    room = get_room_by_id(db, booking_data.room_id)
    if not room.availability:
        raise StayEaseException("Room is not available", status_code=409)

    _ensure_room_has_no_overlap(
        db,
        room_id=booking_data.room_id,
        check_in=booking_data.check_in,
        check_out=booking_data.check_out,
    )

    booking = Booking(
        user_id=current_user.id,
        room_id=booking_data.room_id,
        check_in=booking_data.check_in,
        check_out=booking_data.check_out,
        status=BookingStatus.CONFIRMED,
    )
    db.add(booking)
    db.commit()
    # Refresh loads database-generated values such as id and timestamps.
    db.refresh(booking)
    return booking


def get_my_bookings(
    db: Session,
    current_user: User,
    pagination: PaginationParams,
    status: BookingStatus | None = None,
) -> tuple[list[Booking], int]:
    filters = [Booking.user_id == current_user.id]
    if status is not None:
        filters.append(Booking.status == status)

    count_statement = select(func.count()).select_from(Booking).where(*filters)
    statement = (
        select(Booking)
        .where(*filters)
        .order_by(Booking.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.size)
    )
    return list(db.scalars(statement)), db.scalar(count_statement) or 0


def get_all_bookings(
    db: Session,
    pagination: PaginationParams,
    status: BookingStatus | None = None,
    user_id: int | None = None,
    room_id: int | None = None,
) -> tuple[list[Booking], int]:
    filters = []

    if status is not None:
        filters.append(Booking.status == status)

    if user_id is not None:
        filters.append(Booking.user_id == user_id)

    if room_id is not None:
        filters.append(Booking.room_id == room_id)

    # Admin view: no ownership filter because admins manage platform-wide activity.
    count_statement = select(func.count()).select_from(Booking).where(*filters)
    statement = (
        select(Booking)
        .where(*filters)
        .order_by(Booking.created_at.desc())
        .offset(pagination.offset)
        .limit(pagination.size)
    )
    return list(db.scalars(statement)), db.scalar(count_statement) or 0


def cancel_booking(
    db: Session,
    booking_id: int,
    current_user: User,
) -> Booking:
    booking = _get_booking_for_user(db, booking_id, current_user.id)
    if booking.status == BookingStatus.CANCELLED:
        raise StayEaseException("Booking is already cancelled", status_code=409)

    # Cancellation keeps the booking row for history but stops it from blocking dates.
    booking.status = BookingStatus.CANCELLED
    db.commit()
    db.refresh(booking)
    return booking


def _get_booking_for_user(db: Session, booking_id: int, user_id: int) -> Booking:
    statement = select(Booking).where(
        Booking.id == booking_id,
        Booking.user_id == user_id,
    )
    booking = db.scalar(statement)
    if booking is None:
        raise StayEaseException("Booking not found", status_code=404)
    return booking


def _validate_booking_dates(check_in: date, check_out: date) -> None:
    if check_out <= check_in:
        raise StayEaseException("Check-out date must be after check-in date", status_code=400)


def _ensure_room_has_no_overlap(
    db: Session,
    room_id: int,
    check_in: date,
    check_out: date,
) -> None:
    # Date ranges overlap when an existing booking starts before this one ends
    # and ends after this one starts.
    statement = select(Booking).where(
        Booking.room_id == room_id,
        Booking.status != BookingStatus.CANCELLED,
        Booking.check_in < check_out,
        Booking.check_out > check_in,
    )
    overlapping_booking = db.scalar(statement)
    if overlapping_booking is not None:
        raise StayEaseException("Room is already booked for those dates", status_code=409)
