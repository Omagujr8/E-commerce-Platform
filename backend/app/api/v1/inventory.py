from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies  import get_db
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.services.inventory_service import (
    create_or_replace_inventory,
    update_inventory_setttings,
    increase_stock,
    decrease_stock,
)
from app.repositories.inventory_repo import get_inventory_by_variant_id

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", response_model=InventoryResponse)
def set_inventory(data: InventoryCreate, db: Session = Depends(get_db)):
    try:
        return create_or_replace_inventory(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{variant_id}", response_model=InventoryResponse)
def get_inventory(variant_id: int, db: Session = Depends(get_db)):
    inv = get_inventory_by_variant_id*(db, variant_id)
    if not inv:
        raise HTTPException(status_code = 400, detail = "Inventory not found")
    return inv

@router.patch("/{variant_id}". response_model= InventoryResponse)
def update_inventory(variant_id: int, data: InventoryUpdate, db: Session = Depends(get_db)):
    try:
        return update_inventory_setttings(db, variant_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{variant_id}", response_model=InventoryResponse)
def add_stock(variant_id: int, amount: int, db: Session = Depends(get_db)):
    try:
        return increase_stock(db, variant_id, amount)
    except ValueError as e:
        raise HTTPException(status_code = 400, detail=str(e))

@router.post("/{variant_id}", response_model=InventoryResponse)
def remove_stock(variant_id: int, db: Session = Depends(get_db)):
    try:
        return decrease_stock(db, variant_id, amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
