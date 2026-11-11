from alembic import context
from app.database import engine, Base
from app import models  # noqa: F401

def migrate(connection):
    context.configure(connection=connection, target_metadata=Base.metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


# URL is loaded from the environment, never embedded in the ini or logs.
supplied_connection = context.config.attributes.get('connection')
if supplied_connection is not None:
    migrate(supplied_connection)
else:
    with engine.connect() as connection:
        migrate(connection)
