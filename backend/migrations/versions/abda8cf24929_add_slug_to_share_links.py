"""add_slug_to_share_links

Revision ID: abda8cf24929
Revises: 84cf12782d25
Create Date: 2025-10-15 14:57:03.100979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abda8cf24929'
down_revision: Union[str, Sequence[str], None] = '84cf12782d25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('share_links', sa.Column('slug', sa.String(), nullable=True))
    op.create_index(op.f('ix_share_links_slug'), 'share_links', ['slug'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_share_links_slug'), table_name='share_links')
    op.drop_column('share_links', 'slug')
