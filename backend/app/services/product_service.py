from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.schemas.product import ProductCreate
from app.repositories.product_repo import create_product, get_all_products, get_product_by_id


def create_new_product(db: Session, data: ProductCreate):
    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        category_id=data.category_id,
    )

    variants = [
        ProductVariant(
            name=v.name,
            sku=v.sku,
            extra_price=v.extra_price
        )
        for v in data.variants
    ]

    return create_product(db, product, variants)


def list_products(db: Session):
    return get_all_products(db)


def get_product(db: Session, product_id: int):
    return get_product_by_id(db, product_id)
