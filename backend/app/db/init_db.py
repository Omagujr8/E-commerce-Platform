import logging

from sqlalchemy.exc import OperationalError

from app.db.base import Base
from app.db.session import engine
from app.models import user


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database schema created/verified successfully.")
    except OperationalError as exc:
        logging.error("PostgreSQL connection failed. Please verify DATABASE_URL and docker-compose credentials are aligned.")
        logging.error(f"DATABASE_URL={engine.url}")
        raise
