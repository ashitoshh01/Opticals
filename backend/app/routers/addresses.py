from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.order import AddressCreate, AddressUpdate, AddressResponse
from app.crud.address import get_addresses, create_address, update_address, delete_address
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.get("", response_model=List[AddressResponse])
def list_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_addresses(db, current_user.id)


@router.post("", response_model=AddressResponse, status_code=201)
def add_address(
    data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_address(db, current_user.id, **data.model_dump())


@router.put("/{address_id}", response_model=AddressResponse)
def edit_address(
    address_id: int,
    data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    address = update_address(db, current_user.id, address_id, **data.model_dump())
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.delete("/{address_id}", status_code=204)
def remove_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = delete_address(db, current_user.id, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
