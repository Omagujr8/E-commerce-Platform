from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)

    code = Column(String, unique=True, index=True)

    percentage = Column(Float, nullable=True)
    fixed_amount = Column(Float, nullable=True)

    is_active = Column(Boolean, default=True)

    expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())