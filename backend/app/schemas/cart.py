from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1
    has_power: bool = False


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None
    has_power: Optional[bool] = None


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    has_power: bool
    created_at: datetime
    product: Optional["ProductCartResponse"] = None

    class Config:
        from_attributes = True


class ProductCartResponse(BaseModel):
    id: int
    name: str
    slug: str
    brand: str
    price: float
    discount_price: Optional[float] = None
    color: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class WishlistItemCreate(BaseModel):
    product_id: int


class WishlistItemResponse(BaseModel):
    id: int
    product_id: int
    product: Optional[ProductCartResponse] = None

    class Config:
        from_attributes = True
