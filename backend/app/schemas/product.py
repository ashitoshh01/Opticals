from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True


class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    is_primary: int

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    category_id: int
    name: str
    slug: str
    brand: str
    description: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    gender: Optional[str] = None
    frame_shape: Optional[str] = None
    frame_type: Optional[str] = None
    frame_material: Optional[str] = None
    color: Optional[str] = None
    stock_quantity: int
    rating_avg: float
    promo_tag: Optional[str] = None
    created_at: datetime
    images: List[ProductImageResponse] = []
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
