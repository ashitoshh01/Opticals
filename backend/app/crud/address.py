from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.address import Address


def get_addresses(db: Session, user_id: int) -> List[Address]:
    return db.query(Address).filter(Address.user_id == user_id).all()


def create_address(db: Session, user_id: int, **kwargs) -> Address:
    # If this is default, unset other defaults
    if kwargs.get("is_default"):
        db.query(Address).filter(Address.user_id == user_id).update({"is_default": False})

    address = Address(user_id=user_id, **kwargs)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def update_address(db: Session, user_id: int, address_id: int, **kwargs) -> Optional[Address]:
    address = db.query(Address).filter(Address.id == address_id, Address.user_id == user_id).first()
    if not address:
        return None

    if kwargs.get("is_default"):
        db.query(Address).filter(Address.user_id == user_id).update({"is_default": False})

    for key, value in kwargs.items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)
    return address


def delete_address(db: Session, user_id: int, address_id: int) -> bool:
    address = db.query(Address).filter(Address.id == address_id, Address.user_id == user_id).first()
    if not address:
        return False
    db.delete(address)
    db.commit()
    return True
