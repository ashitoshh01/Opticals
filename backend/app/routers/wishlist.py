from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.cart import WishlistItemCreate, WishlistItemResponse, ProductCartResponse
from app.crud.cart import get_wishlist_items, add_to_wishlist, remove_from_wishlist
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/wishlist", tags=["wishlist"])


def _serialize_wishlist_item(item) -> WishlistItemResponse:
    product_data = None
    if item.product:
        primary_image = None
        if item.product.images:
            primary = next((img for img in item.product.images if img.is_primary), None)
            primary_image = (primary or item.product.images[0]).image_url if item.product.images else None

        product_data = ProductCartResponse(
            id=item.product.id,
            name=item.product.name,
            slug=item.product.slug,
            brand=item.product.brand,
            price=item.product.price,
            discount_price=item.product.discount_price,
            color=item.product.color,
            image_url=primary_image,
        )

    return WishlistItemResponse(
        id=item.id,
        product_id=item.product_id,
        product=product_data,
    )


@router.get("", response_model=List[WishlistItemResponse])
def list_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = get_wishlist_items(db, current_user.id)
    return [_serialize_wishlist_item(i) for i in items]


@router.post("", response_model=WishlistItemResponse, status_code=201)
def add_item(
    data: WishlistItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = add_to_wishlist(db, current_user.id, data.product_id)
    items = get_wishlist_items(db, current_user.id)
    for i in items:
        if i.id == item.id:
            return _serialize_wishlist_item(i)
    return _serialize_wishlist_item(item)


@router.delete("/{product_id}", status_code=204)
def remove_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = remove_from_wishlist(db, current_user.id, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
