"""create post table

Revision ID: cd6577409ce5
Revises: 
Create Date: 2022-10-08 20:24:52.200177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd6577409ce5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
                    , sa.Column('title', sa.String(), nullable=False))
   
    pass
    


def downgrade() -> None:
    pass
