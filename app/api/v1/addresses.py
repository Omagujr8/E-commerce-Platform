from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.auth.dependencies import get_current_user
from app.schemas.address import AddressCreate, AddressResponse
from app.repositories.address_repo import create_address, get_user_addresses

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", response_model=AddressResponse)
def add_address(
    data: AddressCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return create_address(db, user.id, data)


@router.get("/", response_model=list[AddressResponse])
def list_addresses(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_user_addresses(db, user.id)