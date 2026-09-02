from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from app.models.cart import CartItem, WishlistItem
from app.models.product import Product, ProductImage


def get_cart_items(db: Session, user_id: int) -> List[CartItem]:
    return (
        db.query(CartItem)
        .options(joinedload(CartItem.product).joinedload(Product.images))
        .filter(CartItem.user_id == user_id)
        .all()
    )


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1, has_power: bool = False) -> CartItem:
    # Check if item already in cart
    existing = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
        .first()
    )
    if existing:
        existing.quantity += quantity
        db.commit()
        db.refresh(existing)
        return existing

    item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity, has_power=has_power)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_cart_item(db: Session, user_id: int, item_id: int, quantity: Optional[int] = None, has_power: Optional[bool] = None) -> Optional[CartItem]:
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user_id).first()
    if not item:
        return None
    if quantity is not None:
        item.quantity = quantity
    if has_power is not None:
        item.has_power = has_power
    db.commit()
    db.refresh(item)
    return item


def delete_cart_item(db: Session, user_id: int, item_id: int) -> bool:
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def clear_cart(db: Session, user_id: int):
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()


# Wishlist
def get_wishlist_items(db: Session, user_id: int) -> List[WishlistItem]:
    return (
        db.query(WishlistItem)
        .options(joinedload(WishlistItem.product).joinedload(Product.images))
        .filter(WishlistItem.user_id == user_id)
        .all()
    )


def add_to_wishlist(db: Session, user_id: int, product_id: int) -> WishlistItem:
    existing = (
        db.query(WishlistItem)
        .filter(WishlistItem.user_id == user_id, WishlistItem.product_id == product_id)
        .first()
    )
    if existing:
        return existing

    item = WishlistItem(user_id=user_id, product_id=product_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def remove_from_wishlist(db: Session, user_id: int, product_id: int) -> bool:
    item = (
        db.query(WishlistItem)
        .filter(WishlistItem.user_id == user_id, WishlistItem.product_id == product_id)
        .first()
    )
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True
