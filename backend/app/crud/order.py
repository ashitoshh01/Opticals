from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.product import Product
from app.models.address import Address


def create_order_from_cart(db: Session, user_id: int, address_id: int) -> Optional[Order]:
    # Verify address belongs to user
    address = db.query(Address).filter(Address.id == address_id, Address.user_id == user_id).first()
    if not address:
        return None

    # Get cart items
    cart_items = (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == user_id)
        .all()
    )
    if not cart_items:
        return None

    # Calculate total
    total = 0.0
    order_items = []
    for ci in cart_items:
        price = ci.product.discount_price or ci.product.price
        total += price * ci.quantity
        order_items.append(
            OrderItem(
                product_id=ci.product_id,
                quantity=ci.quantity,
                price_at_purchase=price,
            )
        )

    order = Order(
        user_id=user_id,
        address_id=address_id,
        status="placed",
        payment_method="cod",
        total_amount=round(total, 2),
        items=order_items,
    )
    db.add(order)

    # Clear cart
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()

    db.commit()
    db.refresh(order)
    return order


def get_orders(db: Session, user_id: int) -> List[Order]:
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.address),
        )
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )


def get_order_by_id(db: Session, user_id: int, order_id: int) -> Optional[Order]:
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.address),
        )
        .filter(Order.id == order_id, Order.user_id == user_id)
        .first()
    )
