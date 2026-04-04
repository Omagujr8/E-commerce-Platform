from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from app.db.base import Base  # your SQLAlchemy Base
from app.core.config import settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ensure all model modules are imported so SQLAlchemy metadata is up-to-date.
from app.models import user, product, category, order, order_item, inventory, product_variant, payment, review, shipment, discount, address

target_metadata = Base.metadata


def run_migrations_offline():
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    # Always use app config DATABASE_URL (from .env) so alembic and app use same DB.
    connectable = create_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()