"""add foreign key to posts table

Revision ID: 272e0c6b4b95
Revises: cc193d89d5e3
Create Date: 2022-10-09 00:29:05.324822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '272e0c6b4b95'
down_revision = 'cc193d89d5e3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
