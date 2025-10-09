"""add database indexes

Revision ID: add_database_indexes
Revises: add_analytics_fields
Create Date: 2025-10-09 11:35:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'add_database_indexes'
down_revision = 'add_analytics_fields'
branch_label = None
depends_on = None


def upgrade():
    # Composite indexes for common queries
    op.create_index(
        'idx_resume_user_created',
        'resumes',
        ['user_id', sa.text('created_at DESC')],
        unique=False
    )
    
    op.create_index(
        'idx_resume_template',
        'resumes',
        ['template'],
        unique=False
    )
    
    op.create_index(
        'idx_resume_ats_score',
        'resumes',
        [sa.text('ats_score DESC')],
        unique=False,
        postgresql_where=sa.text('ats_score IS NOT NULL')
    )
    
    op.create_index(
        'idx_resume_user_template',
        'resumes',
        ['user_id', 'template'],
        unique=False
    )
    
    # User indexes
    op.create_index(
        'idx_user_email_active',
        'users',
        ['email', 'is_active'],
        unique=False
    )
    
    op.create_index(
        'idx_user_created',
        'users',
        [sa.text('created_at DESC')],
        unique=False
    )


def downgrade():
    op.drop_index('idx_user_created', table_name='users')
    op.drop_index('idx_user_email_active', table_name='users')
    op.drop_index('idx_resume_user_template', table_name='resumes')
    op.drop_index('idx_resume_ats_score', table_name='resumes')
    op.drop_index('idx_resume_template', table_name='resumes')
    op.drop_index('idx_resume_user_created', table_name='resumes')
