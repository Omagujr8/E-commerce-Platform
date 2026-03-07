from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.cart import CartItemAdd, CartResponse
from app.services.cart_service import (
    get_cart,
    add_to_cart,
    update_cart_item,
    remove_from_cart,
)
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

# View item in cart
@router.get("/", response_model=CartResponse)
def view_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_cart(db, user.id)

# Function to add item to cart
@router.post("/add", response_model=CartResponse)
def add_item(item: CartItemAdd, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return add_to_cart(db, user.id, item.variant_id, item.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Function to update item in cart
@router.post("/update", response_model=CartResponse)
def update_item(item: CartItemAdd, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return update_cart_item(db, user.id, item.variant_id, item.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# FUnction to delete item in cart
@router.delete("/remove/{variant_id}", response_model=CartResponse)
def remove_item(variant_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return remove_from_cart(db, user.id, variant_id)