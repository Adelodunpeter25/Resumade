"""add versioning and sharing

Revision ID: add_versioning_and_sharing
Revises: add_oauth_support
Create Date: 2025-10-09 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'add_versioning_and_sharing'
down_revision = 'add_oauth_support'
branch_label = None
depends_on = None


def upgrade():
    # Resume versions table
    op.create_table(
        'resume_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('template', sa.String(), nullable=True),
        sa.Column('personal_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('experience', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('education', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('skills', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('certifications', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('projects', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_resume_versions_id', 'resume_versions', ['id'])
    op.create_index('ix_resume_versions_resume_id', 'resume_versions', ['resume_id'])
    
    # Share links table
    op.create_table(
        'share_links',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.create_index('ix_share_links_id', 'share_links', ['id'])
    op.create_index('ix_share_links_resume_id', 'share_links', ['resume_id'])
    op.create_index('ix_share_links_token', 'share_links', ['token'], unique=True)


def downgrade():
    op.drop_index('ix_share_links_token', table_name='share_links')
    op.drop_index('ix_share_links_resume_id', table_name='share_links')
    op.drop_index('ix_share_links_id', table_name='share_links')
    op.drop_table('share_links')
    
    op.drop_index('ix_resume_versions_resume_id', table_name='resume_versions')
    op.drop_index('ix_resume_versions_id', table_name='resume_versions')
    op.drop_table('resume_versions')
