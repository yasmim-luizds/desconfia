"""Explicit, schema-checked adoption of a C2 database. Back up before invoking."""
from pathlib import Path

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import MetaData, inspect

from .database import Base, engine
from . import models  # noqa: F401


def adopt():
    baseline = MetaData()
    for table in Base.metadata.sorted_tables:
        if table.name != 'ai_quotas':
            copy = table.to_metadata(baseline)
            if table.name == 'analyses':
                copy._columns.remove(copy.c.prompt_version)
    with engine.connect() as connection:
        if 'alembic_version' in inspect(connection).get_table_names():
            raise RuntimeError('Banco já versionado; adoção recusada.')
        differences = compare_metadata(MigrationContext.configure(connection, opts={'compare_type': True}), baseline)
        if differences:
            raise RuntimeError('Esquema diferente da base C2; adoção recusada. Revise uma cópia do banco.')
    command.stamp(Config(str(Path(__file__).resolve().parents[1] / 'alembic.ini')), '0001')
    print('Esquema C2 conferido e marcado como 0001. Execute python -m alembic upgrade head.')


if __name__ == '__main__':
    adopt()
