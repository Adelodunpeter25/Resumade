"""add_section_management_fields

Revision ID: b619abb16615
Revises: 5875baf28297
Create Date: 2025-10-16 19:32:44.978711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b619abb16615'
down_revision: Union[str, Sequence[str], None] = '5875baf28297'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('resumes', sa.Column('section_names', sa.JSON(), nullable=True))
    op.add_column('resumes', sa.Column('custom_sections', sa.JSON(), nullable=True))
    op.add_column('resumes', sa.Column('section_order', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('resumes', 'section_order')
    op.drop_column('resumes', 'custom_sections')
    op.drop_column('resumes', 'section_names')
