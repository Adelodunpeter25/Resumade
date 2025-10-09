"""add analytics fields

Revision ID: add_analytics_fields
Revises: transform_to_resumade
Create Date: 2025-10-09 11:18:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'add_analytics_fields'
down_revision = 'transform_to_resumade'
branch_label = None
depends_on = None


def upgrade():
    op.add_column('resumes', sa.Column('views', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('resumes', sa.Column('downloads', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('resumes', sa.Column('ats_score', sa.Float(), nullable=True))
    op.add_column('resumes', sa.Column('feedback', postgresql.JSON(astext_type=sa.Text()), nullable=True))


def downgrade():
    op.drop_column('resumes', 'feedback')
    op.drop_column('resumes', 'ats_score')
    op.drop_column('resumes', 'downloads')
    op.drop_column('resumes', 'views')
