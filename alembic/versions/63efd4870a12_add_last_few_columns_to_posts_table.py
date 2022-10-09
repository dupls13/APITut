"""add last few columns to posts table

Revision ID: 63efd4870a12
Revises: 272e0c6b4b95
Create Date: 2022-10-09 00:34:02.138193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63efd4870a12'
down_revision = '272e0c6b4b95'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False,
        server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
