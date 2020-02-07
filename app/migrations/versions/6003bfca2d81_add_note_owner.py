"""add_note_owner

Revision ID: 6003bfca2d81
Revises: 1950cfb4aee1
Create Date: 2020-02-06 23:06:04.575528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6003bfca2d81'
down_revision = '1950cfb4aee1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('notes', sa.Column('owner', sa.Integer))


def downgrade():
    op.drop_column('notes', 'owner')

