"""create_notes_table

Revision ID: 88a210ae57b9
Revises: 
Create Date: 2019-03-23 03:59:33.569627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88a210ae57b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("file_name", sa.String(length=255)),
        sa.Column("note_id", sa.String(length=255)),
    )


def downgrade():
    op.drop_table("notes")
