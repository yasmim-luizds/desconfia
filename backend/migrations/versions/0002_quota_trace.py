"""Add persistent budgets and nullable prompt provenance; never backfill guesses."""
from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('analyses', sa.Column('prompt_version', sa.String(40), nullable=True))
    op.create_table('ai_quotas',
        sa.Column('scope', sa.String(20), primary_key=True),
        sa.Column('window_start', sa.Integer(), primary_key=True),
        sa.Column('used', sa.Integer(), nullable=False))


def downgrade():
    raise RuntimeError('Downgrade destrutivo bloqueado. Reverta o código mantendo as colunas aditivas ou restaure backup isolado.')
