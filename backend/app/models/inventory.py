from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    variant_id = Column(Integer, ForeignKey("product_variants.id"), unique=True, nullable=False)

    stock_quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=5)

    updated_at = Column(DateTime(timezone =True), onupdate=func.now(), server_default = func.now())

    variant = relationship("ProductVariant", backref="inventory")
