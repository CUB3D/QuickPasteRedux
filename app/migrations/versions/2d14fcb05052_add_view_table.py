"""Add view table

Revision ID: 2d14fcb05052
Revises: becdc669f4b5
Create Date: 2020-04-06 13:35:49.006211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d14fcb05052'
down_revision = 'becdc669f4b5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "views",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("note_id", sa.Integer, sa.ForeignKey("notes.id")),
        sa.Column("visitor_id", sa.String(length=64)),
        sa.Column("created", sa.DateTime())
    )


def downgrade():
    op.drop_table("views")
