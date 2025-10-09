"""add oauth support

Revision ID: add_oauth_support
Revises: add_database_indexes
Create Date: 2025-10-09 11:36:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'add_oauth_support'
down_revision = 'add_database_indexes'
branch_label = None
depends_on = None


def upgrade():
    # Make hashed_password nullable for OAuth users
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.String(),
                    nullable=True)
    
    # Add OAuth fields
    op.add_column('users', sa.Column('oauth_provider', sa.String(), nullable=True))
    op.add_column('users', sa.Column('oauth_id', sa.String(), nullable=True))
    
    # Add index for OAuth lookups
    op.create_index('idx_user_oauth', 'users', ['oauth_provider', 'oauth_id'], unique=False)


def downgrade():
    op.drop_index('idx_user_oauth', table_name='users')
    op.drop_column('users', 'oauth_id')
    op.drop_column('users', 'oauth_provider')
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.String(),
                    nullable=False)
