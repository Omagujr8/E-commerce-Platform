from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    name = Column(String, nullable=False)  # e.g "Red - XL"
    sku = Column(String, unique=True, index=True)

    extra_price = Column(Float, default=0.0)

    product = relationship("Product", back_populates="variants")
