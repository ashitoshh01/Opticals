import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.database import get_db
from app.schemas.product import ProductResponse, ProductListResponse
from app.schemas.review import ReviewCreate, ReviewResponse
from app.crud.product import get_products, get_product_by_slug
from app.crud.review import get_reviews_for_product, create_review
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductListResponse)
def list_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    frame_shape: Optional[str] = None,
    gender: Optional[str] = None,
    frame_type: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=48),
    db: Session = Depends(get_db),
):
    products, total = get_products(
        db,
        category=category,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        frame_shape=frame_shape,
        gender=gender,
        frame_type=frame_type,
        sort=sort,
        page=page,
        page_size=page_size,
    )
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    return ProductListResponse(
        products=products,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{slug}", response_model=ProductResponse)
def get_product(slug: str, db: Session = Depends(get_db)):
    product = get_product_by_slug(db, slug)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/{product_id}/reviews", response_model=List[ReviewResponse])
def list_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = get_reviews_for_product(db, product_id)
    result = []
    for r in reviews:
        data = ReviewResponse.model_validate(r)
        data.user_name = r.user.name if r.user else None
        result.append(data)
    return result


@router.post("/{product_id}/reviews", response_model=ReviewResponse, status_code=201)
def add_review(
    product_id: int,
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    review = create_review(db, product_id=product_id, user_id=current_user.id, rating=data.rating, comment=data.comment)
    result = ReviewResponse.model_validate(review)
    result.user_name = current_user.name
    return result
