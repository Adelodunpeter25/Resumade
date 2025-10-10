"""create resume progress table

Revision ID: create_resume_progress_001
Revises: 
Create Date: 2025-10-10 11:47:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = 'create_resume_progress_001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create resume_progress table
    op.create_table(
        'resume_progress',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('completion_percentage', sa.Float(), nullable=False, server_default='0'),
        sa.Column('section_scores', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resume_progress_id'), 'resume_progress', ['id'], unique=False)
    op.create_index(op.f('ix_resume_progress_resume_id'), 'resume_progress', ['resume_id'], unique=True)

def downgrade():
    # Drop resume_progress table
    op.drop_index(op.f('ix_resume_progress_resume_id'), table_name='resume_progress')
    op.drop_index(op.f('ix_resume_progress_id'), table_name='resume_progress')
    op.drop_table('resume_progress')
