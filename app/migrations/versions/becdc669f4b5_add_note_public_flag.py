"""add_note_public_flag

Revision ID: becdc669f4b5
Revises: 6003bfca2d81
Create Date: 2020-04-04 17:01:40.678401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'becdc669f4b5'
down_revision = '6003bfca2d81'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('notes', sa.Column('public', sa.Boolean))


def downgrade():
    op.drop_column('notes', 'public')
