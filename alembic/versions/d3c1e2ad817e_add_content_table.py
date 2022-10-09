"""add content table

Revision ID: d3c1e2ad817e
Revises: cd6577409ce5
Create Date: 2022-10-08 20:34:05.338019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3c1e2ad817e'
down_revision = 'cd6577409ce5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_column('posts', 'content')
    pass