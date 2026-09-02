from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartItemResponse, WishlistItemCreate, WishlistItemResponse, ProductCartResponse
from app.crud.cart import get_cart_items, add_to_cart, update_cart_item, delete_cart_item, get_wishlist_items, add_to_wishlist, remove_from_wishlist
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/cart", tags=["cart"])


def _serialize_cart_item(item) -> CartItemResponse:
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

    return CartItemResponse(
        id=item.id,
        product_id=item.product_id,
        quantity=item.quantity,
        has_power=item.has_power,
        created_at=item.created_at,
        product=product_data,
    )


@router.get("", response_model=List[CartItemResponse])
def list_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = get_cart_items(db, current_user.id)
    return [_serialize_cart_item(i) for i in items]


@router.post("", response_model=CartItemResponse, status_code=201)
def add_item(
    data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = add_to_cart(db, current_user.id, data.product_id, data.quantity, data.has_power)
    # Re-fetch with product loaded
    items = get_cart_items(db, current_user.id)
    for i in items:
        if i.id == item.id:
            return _serialize_cart_item(i)
    return _serialize_cart_item(item)


@router.patch("/{item_id}", response_model=CartItemResponse)
def update_item(
    item_id: int,
    data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = update_cart_item(db, current_user.id, item_id, quantity=data.quantity, has_power=data.has_power)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    items = get_cart_items(db, current_user.id)
    for i in items:
        if i.id == item.id:
            return _serialize_cart_item(i)
    return _serialize_cart_item(item)


@router.delete("/{item_id}", status_code=204)
def remove_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = delete_cart_item(db, current_user.id, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found")
