from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import StayEaseException
from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate


def get_properties(db: Session) -> list[Property]:
    statement = select(Property).order_by(Property.created_at.desc())
    return list(db.scalars(statement))


def get_property_by_id(db: Session, property_id: int) -> Property:
    property_item = db.get(Property, property_id)
    if property_item is None:
        raise StayEaseException("Property not found", status_code=404)
    return property_item


def create_property(db: Session, property_data: PropertyCreate) -> Property:
    property_item = Property(**property_data.model_dump())
    db.add(property_item)
    db.commit()
    # Refresh loads database-generated values such as id and created_at.
    db.refresh(property_item)
    return property_item


def update_property(
    db: Session,
    property_id: int,
    property_data: PropertyUpdate,
) -> Property:
    property_item = get_property_by_id(db, property_id)

    # exclude_unset keeps omitted fields unchanged during partial updates.
    update_data = property_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(property_item, field, value)

    db.commit()
    db.refresh(property_item)
    return property_item


def delete_property(db: Session, property_id: int) -> None:
    property_item = get_property_by_id(db, property_id)
    db.delete(property_item)
    db.commit()
