
import sqlalchemy

metadata = sqlalchemy.MetaData()

note = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("file_name", sqlalchemy.String(length=255)),
    sqlalchemy.Column("note_id", sqlalchemy.String(length=255), unique=True),
    sqlalchemy.Column('security_key', sqlalchemy.String(length=255)),
    sqlalchemy.Column("owner", sqlalchemy.Integer),
    sqlalchemy.Column("public", sqlalchemy.Boolean)
)

view = sqlalchemy.Table(
    "views",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("note_id", sqlalchemy.Integer(), sqlalchemy.ForeignKey("notes.id")),
    sqlalchemy.Column("visitor_id", sqlalchemy.String(length=64)),
    sqlalchemy.Column("created", sqlalchemy.DateTime())
)
