import math
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List, Tuple

from app.models.product import Product, ProductImage
from app.models.category import Category


def get_categories(db: Session) -> List[Category]:
    return db.query(Category).all()


def get_category_by_slug(db: Session, slug: str) -> Optional[Category]:
    return db.query(Category).filter(Category.slug == slug).first()


def get_products(
    db: Session,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    frame_shape: Optional[str] = None,
    gender: Optional[str] = None,
    frame_type: Optional[str] = None,
    sort: Optional[str] = None,
    page: int = 1,
    page_size: int = 12,
) -> Tuple[List[Product], int]:
    query = db.query(Product).options(joinedload(Product.images), joinedload(Product.category))

    if category:
        query = query.join(Category).filter(Category.slug == category)
    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if frame_shape:
        query = query.filter(Product.frame_shape.ilike(frame_shape))
    if gender:
        query = query.filter(Product.gender.ilike(gender))
    if frame_type:
        query = query.filter(Product.frame_type.ilike(frame_type))

    total = query.count()

    # Sorting
    if sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())
    elif sort == "rating":
        query = query.order_by(Product.rating_avg.desc())
    elif sort == "newest":
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    offset = (page - 1) * page_size
    products = query.offset(offset).limit(page_size).all()

    return products, total


def get_product_by_slug(db: Session, slug: str) -> Optional[Product]:
    return (
        db.query(Product)
        .options(joinedload(Product.images), joinedload(Product.category))
        .filter(Product.slug == slug)
        .first()
    )


def search_products(db: Session, q: str, page: int = 1, page_size: int = 12) -> Tuple[List[Product], int]:
    query = (
        db.query(Product)
        .options(joinedload(Product.images), joinedload(Product.category))
        .filter(
            (Product.name.ilike(f"%{q}%"))
            | (Product.brand.ilike(f"%{q}%"))
            | (Product.description.ilike(f"%{q}%"))
        )
    )
    total = query.count()
    offset = (page - 1) * page_size
    products = query.order_by(Product.created_at.desc()).offset(offset).limit(page_size).all()
    return products, total
