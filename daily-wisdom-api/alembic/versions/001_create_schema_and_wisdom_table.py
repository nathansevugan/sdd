"""Create schema and wisdom table

Revision ID: 001_create_schema_and_wisdom_table
Revises: 
Create Date: 2026-05-10 21:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_create_schema_and_wisdom_table'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create schema
    op.execute('CREATE SCHEMA IF NOT EXISTS app')
    
    # Create wisdom_entries table
    op.create_table(
        'wisdom_entries',
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='app'
    )
    
    # Create indexes
    op.create_index('idx_wisdom_entries_deleted_at', 'wisdom_entries', ['deleted_at'], 
                   unique=False, schema='app', postgresql_where=sa.text('deleted_at IS NULL'))


def downgrade() -> None:
    op.drop_table('wisdom_entries', schema='app')
    # Note: We don't drop the schema to be safe
