"""add_index_resume_progress_resume_id

Revision ID: 26348005d948
Revises: 3f95d27c640f
Create Date: 2025-10-13 19:57:13.380336

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26348005d948'
down_revision: Union[str, Sequence[str], None] = '3f95d27c640f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check if table exists before creating index
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'resume_progress' in inspector.get_table_names():
        op.create_index('ix_resume_progress_resume_id', 'resume_progress', ['resume_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if 'resume_progress' in inspector.get_table_names():
        op.drop_index('ix_resume_progress_resume_id', table_name='resume_progress')
