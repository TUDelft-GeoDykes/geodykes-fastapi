import os
import re
from logging.config import fileConfig

from alembic import context
from sqlalchemy import URL, create_engine

from app.db.base import Base
from app.apps.decks.models import Deck, Card
from app.apps.dykes.models import Dyke, Crossection

from app.settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def get_dsn() -> URL:
    db_dsn = settings.db_dsn
    return db_dsn.set(drivername="postgresql")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    context.configure(
        url=get_dsn(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode. In this scenario we need to create 
    an Engine and associate a connection with the context.
    """

    url_tokens = {
        "DB_USER": os.getenv("DB_USER", ""),
        "DB_PASS": os.getenv("DB_PASS", ""),
        "DB_HOST": os.getenv("DB_HOST", ""),
        "DB_NAME": os.getenv("DB_NAME", "")
    }

    url = config.get_main_option("sqlalchemy.url")

    url = re.sub(r"\${(.+?)}", lambda m: url_tokens[m.group(1)], url)

    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
