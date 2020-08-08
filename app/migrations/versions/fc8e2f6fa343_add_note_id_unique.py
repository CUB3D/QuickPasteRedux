"""Add note_id unique

Revision ID: fc8e2f6fa343
Revises: 2d14fcb05052
Create Date: 2020-04-06 15:35:35.712392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc8e2f6fa343'
down_revision = '2d14fcb05052'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        table_name='notes',
        column_name='note_id',
        nullable=False,
        unique=True,
        type_=sa.String(length=255)
    )


def downgrade():
    pass
