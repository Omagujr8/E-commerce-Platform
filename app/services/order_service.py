from sqlalchemy.orm import Session

from app.services.cart_service import get_cart, clear_cart
from app.repositories.inventory_repo import get_inventory_by_variant_id
from app.repositories.order_repo import create_order
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product_variant import ProductVariant
from app.repositories.address_repo import get_address_by_id
from app.services.shipping_service import calculate_shipping
from app.repositories.discount_repo import get_discount_by_code, is_valid_discount
from app.services.discount_service import apply_discount

def checkout(db: Session, user_id: int, address_id: int, discount_code: str = None):

    address = get_address_by_id(db, address_id)

    if not address:
        raise ValueError("Invalid address")

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
            raise ValueError("Insufficient stock")

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

        inv.stock_quantity -= quantity

    shipping_cost = calculate_shipping(address.state, total_amount)

    order = Order(
        user_id=user_id,
        total_amount=total_amount + shipping_cost,
        status="PENDING_PAYMENT",
        address_id=address.id,
        shipping_cost=shipping_cost
    )

    discount_amount = 0

    if discount_code:
        discount = get_discount_by_code(db, discount_code)

        if not is_valid_discount(discount):
            raise ValueError("Invalid or expired discount code")

        new_total = apply_discount(total_amount, discount)
        discount_amount = total_amount - new_total
        total_amount = new_total

    created = create_order(db, order, items)

    clear_cart(user_id)

    return created