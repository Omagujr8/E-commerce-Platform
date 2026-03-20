from sqlalchemy.orm import Session

from app.services.cart_service import get_cart, clear_cart
from app.repositories.inventory_repo import get_inventory_by_variant_id
from app.repositories.order_repo import create_order
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product_variant import ProductVariant


def checkout(db: Session, user_id: int):

    cart = get_cart(db, user_id)

    if not cart["items"]:
        raise ValueError("Cart is empty")

    items = []
    total_amount = 0

    for item in cart["items"]:

        variant_id = item["variant_id"]
        quantity = item["quantity"]

        inv = get_inventory_by_variant_id(db, variant_id)

        if not inv or inv.stock_quantity < quantity:
            raise ValueError(f"Insufficient stock for variant {variant_id}")

        variant = db.query(ProductVariant).filter(
            ProductVariant.id == variant_id
        ).first()

        price = variant.extra_price + variant.product.price

        total_amount += price * quantity

        items.append(
            OrderItem(
                variant_id=variant_id,
                quantity=quantity,
                price=price
            )
        )

        # Deduct stock
        inv.stock_quantity -= quantity

    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="PENDING_PAYMENT"
    )

    created = create_order(db, order, items)

    clear_cart(user_id)

    return created