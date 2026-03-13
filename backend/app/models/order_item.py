from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=False)

    quantity = Column(Integer, nullable=False)

    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")