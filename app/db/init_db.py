import logging

from sqlalchemy.exc import OperationalError

from app.db.base import Base
from app.db.session import engine

# Import all models exactly once in startup so Base.metadata is fully populated
from app.models import user, product, category, order, order_item, inventory, product_variant, payment, review, shipment, discount


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database schema created/verified successfully.")
    except OperationalError as exc:
        logging.error("PostgreSQL connection failed. Please verify DATABASE_URL and docker-compose credentials are aligned.")
        logging.error(f"DATABASE_URL={engine.url}")
        raise
