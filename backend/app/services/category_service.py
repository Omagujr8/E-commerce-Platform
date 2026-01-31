from sqlalchemy.orm import Session
from models.category import Category
from app.schemas.category import CategoryCreate
from app.repositories.category_repo import create_category, get_all_categories

def create_new_category(db: Session, data: CategoryCreate):
    category = Category(
        name=data.name,
        parent_id=data.parent_id,
    )
    return create_category(db, category)

def list_categories(db: Session):
    return get_all_categories(db)

