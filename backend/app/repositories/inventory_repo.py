from sqlalchemy.orm import Session
from app.models.inventory import Inventory

def get_inventory_by_variant_id(db:Session, variant_id:int):
    return db.query(Inventory).filter(Inventory.variant_id == variant_id).first()

def create_inventory(db: Session, inv: Inventory):
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

def update_inventory(db: Session, inv: Inventory):
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

