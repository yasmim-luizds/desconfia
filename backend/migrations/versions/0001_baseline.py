"""Original C2 schema. Existing databases need audited baseline adoption."""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('full_name', sa.String(120), nullable=False),
        sa.Column('email', sa.String(254), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_table('analyses',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('message_text', sa.Text(), nullable=False),
        sa.Column('risk_level', sa.String(10), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.Column('recommendation', sa.Text(), nullable=False),
        sa.Column('ai_provider', sa.String(40), nullable=False),
        sa.Column('ai_model', sa.String(100)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime()))
    op.create_index('ix_analyses_user_id', 'analyses', ['user_id'])
    op.create_table('analysis_indicators',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('analysis_id', sa.String(36), sa.ForeignKey('analyses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('category', sa.String(40), nullable=False),
        sa.Column('description', sa.String(240), nullable=False),
        sa.Column('evidence', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=False))
    op.create_index('ix_analysis_indicators_analysis_id', 'analysis_indicators', ['analysis_id'])
    op.create_table('feedbacks',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('analysis_id', sa.String(36), sa.ForeignKey('analyses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('is_helpful', sa.Boolean(), nullable=False),
        sa.Column('comment', sa.String(1000)),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('analysis_id', 'user_id', name='ux_feedback_analysis_user'))


def downgrade():
    raise RuntimeError('Remoção do esquema base bloqueada; restaure um backup em ambiente isolado.')
