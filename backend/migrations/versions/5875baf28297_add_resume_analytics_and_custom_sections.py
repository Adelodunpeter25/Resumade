"""add_resume_analytics_and_custom_sections

Revision ID: 5875baf28297
Revises: abda8cf24929
Create Date: 2025-10-16 19:07:27.578908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5875baf28297'
down_revision: Union[str, Sequence[str], None] = 'abda8cf24929'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create resume_analytics table
    op.create_table(
        'resume_analytics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('share_token', sa.String(), nullable=True),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resume_analytics_id'), 'resume_analytics', ['id'], unique=False)
    op.create_index(op.f('ix_resume_analytics_resume_id'), 'resume_analytics', ['resume_id'], unique=False)
    op.create_index(op.f('ix_resume_analytics_share_token'), 'resume_analytics', ['share_token'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_resume_analytics_share_token'), table_name='resume_analytics')
    op.drop_index(op.f('ix_resume_analytics_resume_id'), table_name='resume_analytics')
    op.drop_index(op.f('ix_resume_analytics_id'), table_name='resume_analytics')
    op.drop_table('resume_analytics')
