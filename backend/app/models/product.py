from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)

    price = Column(Float, nullable=False)

    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey("categories.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", backref="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete")
