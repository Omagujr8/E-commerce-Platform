from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.repositories.inventory_repo import (
    get_inventory_by_variant_id,
    create_inventory,
    update_inventory,
)
from app.schemas.inventory import InventoryCreate, InventoryUpdate
from watchfiles.run import detect_target_type


def create_or_replace_inventory(db: Session, data: InventoryCreate):
    existing = get_inventory_by_variant_id(db, data.variant_id)

    if existing:
        existing.stock_quantity = data.stock_quantity
        existing.low_stock_threshold = data.low_stock_threshold
        return update_inventory(db, existing)

    inv = Inventory(
        variant_id = data.variant_id,
        stock_quantity = data.stock_quantity,
        low_stock_threshold = data.low_stock_threshold,
    )
    return create_inventory(db, inv)

def update_inventory_settings(db: Session, variant_id: int, data: InventoryUpdate):
    inv = get_inventory_by_variant_id(db, variant_id)
    if not inv:
        raise ValueError("Inventory record not found")

    if data.stock_quantity is not None:
        if data.stock_quantity < 0:
            raise ValueError ("Stock cannot be negative")
        inv.stock_quantity = data.stock_quantity

    if data.low_stock_threshold is not None:
        if data.low_stock_threshold < 0:
            raise ValueError ("Low stock threshold cannot be negative")
        inv.low_stock_threshold = data.low_stock_threshold

    return update_inventory(db, inv)

def increase_stock(db: Session, variant_id: int, amount: int):
    if amount <= 0:
        raise ValueError ("Increase amount must be > o")
    inv = get_inventory_by_variant_id(db, variant_id)
    if not inv:
        raise ValueError("Inventory record not found")

    inv.stock_quantity += amount
    return update_inventory(db, inv)


def decrease_stock(db: Session, variant_id: int, amount: int):
    if amount <= 0:
        raise ValueError("Decrease amount must be > 0")

    inv = get_inventory_by_variant_id(db, variant_id)
    if not inv:
        raise ValueError("Inventory record not found")

    if inv.stock_quantity < amount:
        raise ValueError("Insufficient stock")

    inv.stock_quantity -= amount
    return update_inventory(db, inv)


def is_low_stock(inv: Inventory) -> bool:
    return inv.stock_quantity <= inv.low_stock_threshold
