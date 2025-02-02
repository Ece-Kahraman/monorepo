from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from alembic.operations import ops

import os
from dotenv import load_dotenv

import sys
from pathlib import Path

monorepo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(monorepo_root))

from core.database import Base
from core.ledgers.models import LedgerEntryModel

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# !!! Force the Alembic Config object to use the .env db url !!!
_url = "postgresql://" + str(os.environ.get("_DATABASE_URL"))
config.set_main_option("sqlalchemy.url", _url)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def exclude_other_app_tables(context, revision, directives):
    # Get the current app's version table name (e.g., "alembic_version_app1")
    current_version_table = context.config.get_main_option("version_table")

    # List all tables to exclude (other apps' version tables)
    excluded_tables = {"alembic_version_app1", "alembic_version_app2"} - {current_version_table}

    for directive in directives:
        if isinstance(directive, ops.MigrationScript):
            if directive.upgrade_ops:
                directive.upgrade_ops.ops = [
                    op for op in directive.upgrade_ops.ops
                    if not (isinstance(op, ops.DropTableOp) and op.table_name in excluded_tables)
                ]

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata, 
            version_table="alembic_version_app1",
            process_revision_directives=exclude_other_app_tables
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
