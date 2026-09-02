from sqlalchemy.orm import Session
from sqlalchemy import func as sqla_func
from typing import List

from app.models.review import Review
from app.models.product import Product


def get_reviews_for_product(db: Session, product_id: int) -> List[Review]:
    return (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .all()
    )


def create_review(db: Session, product_id: int, user_id: int, rating: int, comment: str = None) -> Review:
    review = Review(
        product_id=product_id,
        user_id=user_id,
        rating=rating,
        comment=comment,
    )
    db.add(review)
    db.commit()

    # Update product rating average
    avg = db.query(sqla_func.avg(Review.rating)).filter(Review.product_id == product_id).scalar()
    product = db.query(Product).filter(Product.id == product_id).first()
    if product and avg:
        product.rating_avg = round(float(avg), 1)
        db.commit()

    db.refresh(review)
    return review
