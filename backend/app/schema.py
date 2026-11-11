"""Schema lifecycle: explicit migration in production, empty local DB convenience."""
from pathlib import Path

from alembic.config import Config
from alembic import command
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import inspect

from .database import Base


def prepare_schema(engine, production: bool) -> None:
    # Import models to register all tables without importing the HTTP application.
    from . import models  # noqa: F401
    with engine.connect() as connection:
        tables = set(inspect(connection).get_table_names())
        if not production and not tables:
            config = Config(str(Path(__file__).resolve().parents[1] / 'alembic.ini'))
            config.attributes['connection'] = connection
            command.upgrade(config, 'head')
            connection.commit()
            return
        if production:
            config = Config(str(Path(__file__).resolve().parents[1] / 'alembic.ini'))
            expected = set(ScriptDirectory.from_config(config).get_heads())
            current = set(MigrationContext.configure(connection).get_current_heads())
            if current != expected:
                raise RuntimeError('Banco desatualizado. Consulte backend/README.md antes de migrar.')
        # A local legacy DB must also be upgraded explicitly, never silently altered.
        inspector = inspect(connection)
        for table in Base.metadata.sorted_tables:
            if table.name not in tables:
                raise RuntimeError('Banco desatualizado. Consulte backend/README.md antes de migrar.')
            actual = {c['name'] for c in inspector.get_columns(table.name)}
            if not set(table.columns.keys()).issubset(actual):
                raise RuntimeError('Banco desatualizado. Consulte backend/README.md antes de migrar.')
