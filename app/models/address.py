from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, default="Nigeria")

    is_default = Column(Boolean, default=False)

    user = relationship("User")