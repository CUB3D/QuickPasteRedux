# from gino import Gino
# import asyncio
#
# db = Gino()
#
#
# class Note(db.Model):
#     __tablename__ = "notes"
#
#     id = db.Column(db.Integer(), primary_key=True)
#     file_name = db.Column(db.Unicode())
#     note_id = db.Column(db.Unicode())
#
#
# async def main():
#     #await db.set_bind("postgresql://172.18.0.1/quickpaste")
#     await db.set_bind("sqlite:///quickpaste.db")
#     #TODO: alembic
#     await db.gino.create_all()
#
# asyncio.get_event_loop().run_until_complete(main())

import sqlalchemy

metadata = sqlalchemy.MetaData()

note = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("file_name", sqlalchemy.String(length=255)),
    sqlalchemy.Column("note_id", sqlalchemy.String(length=255)),
    sqlalchemy.Column('security_key', sqlalchemy.String(length=128)),
    sqlalchemy.Column("owner", sqlalchemy.Integer)
)
