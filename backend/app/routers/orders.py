from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderItemResponse
from app.crud.order import create_order_from_cart, get_orders, get_order_by_id
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])


def _serialize_order(order) -> OrderResponse:
    items = []
    for oi in order.items:
        product_name = oi.product.name if oi.product else None
        product_image = None
        if oi.product and oi.product.images:
            primary = next((img for img in oi.product.images if img.is_primary), None)
            product_image = (primary or oi.product.images[0]).image_url if oi.product.images else None

        items.append(OrderItemResponse(
            id=oi.id,
            product_id=oi.product_id,
            quantity=oi.quantity,
            price_at_purchase=oi.price_at_purchase,
            product_name=product_name,
            product_image=product_image,
        ))

    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        address_id=order.address_id,
        status=order.status,
        payment_method=order.payment_method,
        total_amount=order.total_amount,
        created_at=order.created_at,
        items=items,
        address=order.address,
    )


@router.post("", response_model=OrderResponse, status_code=201)
def place_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = create_order_from_cart(db, current_user.id, data.address_id)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty or address not found")
    # Re-fetch to get all relationships loaded
    order = get_order_by_id(db, current_user.id, order.id)
    return _serialize_order(order)


@router.get("", response_model=List[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = get_orders(db, current_user.id)
    return [_serialize_order(o) for o in orders]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = get_order_by_id(db, current_user.id, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _serialize_order(order)
