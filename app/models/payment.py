from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    provider = Column(String, default="stripe")

    amount = Column(Float, nullable=False)

    status = Column(String, default="pending")

    payment_intent_id = Column(String, unique=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())