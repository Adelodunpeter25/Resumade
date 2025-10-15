"""merge_heads

Revision ID: 7996f95d3283
Revises: add_versioning_and_sharing, create_resume_progress_001
Create Date: 2025-10-13 12:02:34.098086

"""
from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = '7996f95d3283'
down_revision: Union[str, Sequence[str], None] = ('add_versioning_and_sharing', 'create_resume_progress_001')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
