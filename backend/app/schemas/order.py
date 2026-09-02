from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    is_default: bool = False


class AddressUpdate(AddressCreate):
    pass


class AddressResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    phone: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    is_default: bool

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    address_id: int


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_purchase: float
    product_name: Optional[str] = None
    product_image: Optional[str] = None

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    address_id: int
    status: str
    payment_method: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse] = []
    address: Optional[AddressResponse] = None

    class Config:
        from_attributes = True
