import json
from sqlalchemy.orm import Session
from app.utils.cache import redis_client
from app.repositories.inventory_repo import get_inventory_by_variant_id

from backend.app.schemas.cart import CartResponse


def _cart_key(user_id: id) -> str:
    return f"cart_{user_id}"

# getting the item the cart
def get_cart(db: Session, user_id: id):
    key = _cart_key(user_id)
    raw = redis_client.get(key)

    if not raw:
        return {"user_id": user_id, "items": []}

    data = json.loads(raw)

    items = [
        {"variant_id": int(variant_id), "quantity": qty}
        for variant_id, qty in data.get("items", {}).items()
    ]
    return {"user_id": user_id, "items": items}

# Adding item to cart
def add_cart(db: Session, user_id: int, variant_id: int, quantity: int):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    #validate stock
    inv = get_inventory_by_variant_id(db, variant_id)
    if not inv:
        raise ValueError("Variant inventory not found")

    if inv.stock_quantity < quantity:
        raise ValueError("Not enough stock available")

    key = _cart_key(user_id)
    raw = redis_client.get(key)

    if raw:
        data = json.loads(raw)
    else:
        data = {"items": {}}

    current_qty = data["items"].get(str(variant_id), 0)
    new_qty = current_qty + quantity

    if inv.stock_quantity < new_qty:
        raise ValueError("Not enough stock available for requested quantity")

    data["items"][str(variant_id)] = new_qty

    redis_client.set(key, json.dumps(data))
    return get_cart(db, user_id)

# Updating items in cart
def update_cart_item(db: Session, user_id: int, variant_id: int, quantity: int):
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    inv = get_inventory_by_variant_id(db, variant_id)
    if not inv:
        raise ValueError("Variant inventory not found")

    if inv.stock_quantity < quantity:
        raise ValueError("Not enough stock available")

    key = _cart_key(user_id)
    raw = redis_client.get(key)

    if not raw:
        data = {"items": {}}
    else:
        data = json.loads(raw)

    if quantity == 0:
        data["items"].pop(str(variant_id), None)
    else:
        data["items"][str(variant_id)] = quantity

    redis_client.set(key, json.dumps(data))
    return get_cart(db, user_id)

# Removing item from cart
def remove_from_cart(db: Session, user_id: int, variant_id: int):
    key = _cart_key(user_id)
    raw = redis_client.get(key)

    if not raw:
        return get_cart(db, user_id)

    data = json.loads(raw)
    data["items"].pop(str(variant_id), None)

    redis_client.set(key, json.dumps(data))
    return get_cart(db, user_id)

# Clearing the item in cart or deleting cart
def clear_cart(user_id: int):
    key = _cart_key(user_id)
    redis_client.delete(key)