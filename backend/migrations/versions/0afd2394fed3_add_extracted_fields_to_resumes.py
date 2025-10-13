"""add_extracted_fields_to_resumes

Revision ID: 0afd2394fed3
Revises: 26348005d948
Create Date: 2025-10-13 19:59:28.340484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0afd2394fed3'
down_revision: Union[str, Sequence[str], None] = '26348005d948'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    if 'resumes' in inspector.get_table_names():
        # Add new columns
        op.add_column('resumes', sa.Column('full_name', sa.String(), nullable=True))
        op.add_column('resumes', sa.Column('email', sa.String(), nullable=True))
        op.add_column('resumes', sa.Column('template_name', sa.String(), nullable=True, server_default='professional-blue'))
        
        # Create indexes
        op.create_index('ix_resumes_full_name', 'resumes', ['full_name'], unique=False)
        op.create_index('ix_resumes_email', 'resumes', ['email'], unique=False)
        op.create_index('ix_resumes_template_name', 'resumes', ['template_name'], unique=False)
        op.create_index('ix_resumes_created_at', 'resumes', ['created_at'], unique=False)
        op.create_index('ix_resumes_updated_at', 'resumes', ['updated_at'], unique=False)
        
        # Populate extracted fields from JSON
        conn.execute(sa.text("""
            UPDATE resumes 
            SET full_name = personal_info->>'full_name',
                email = personal_info->>'email'
            WHERE personal_info IS NOT NULL
        """))


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    if 'resumes' in inspector.get_table_names():
        op.drop_index('ix_resumes_updated_at', table_name='resumes')
        op.drop_index('ix_resumes_created_at', table_name='resumes')
        op.drop_index('ix_resumes_template_name', table_name='resumes')
        op.drop_index('ix_resumes_email', table_name='resumes')
        op.drop_index('ix_resumes_full_name', table_name='resumes')
        op.drop_column('resumes', 'template_name')
        op.drop_column('resumes', 'email')
        op.drop_column('resumes', 'full_name')
