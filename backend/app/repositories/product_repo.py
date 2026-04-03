from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product_variant import ProductVariant


def create_product(db: Session, product: Product, variants: list[ProductVariant]):
    db.add(product)
    db.flush()  # get product.id

    for variant in variants:
        variant.product_id = product.id
        db.add(variant)

    db.commit()
    db.refresh(product)
    return product


def get_all_products(db: Session):
    return db.query(Product).filter(Product.is_active == True).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()
