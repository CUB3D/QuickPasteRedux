"""add_security_key

Revision ID: 1950cfb4aee1
Revises: 88a210ae57b9
Create Date: 2019-03-25 04:42:51.203796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1950cfb4aee1'
down_revision = '88a210ae57b9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('notes', sa.Column('security_key', sa.String(128)))


def downgrade():
    op.drop_column('notes', 'security_key')
