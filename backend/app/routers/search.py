import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.schemas.product import ProductListResponse
from app.crud.product import search_products

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=ProductListResponse)
def search(
    q: str = Query("", min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=48),
    db: Session = Depends(get_db),
):
    products, total = search_products(db, q=q, page=page, page_size=page_size)
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    return ProductListResponse(
        products=products,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )
