from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse, RedirectResponse, PlainTextResponse
from starlette.config import Config
from starlette.templating import Jinja2Templates
import os
import string
import random
import uuid
from databases import Database

config = Config(os.environ["ENV"])
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL")

app = Starlette(debug=DEBUG)
templates = Jinja2Templates("templates")

database = Database(DATABASE_URL)

import sqlalchemy

metadata = sqlalchemy.MetaData()

note = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("file_name", sqlalchemy.String(length=255)),
    sqlalchemy.Column("note_id", sqlalchemy.String(length=255))
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.route("/")
async def root(req):
    return templates.TemplateResponse("main.html", {"request": req})


@app.route("/resource/{file}")
async def resource(req):
    return FileResponse(os.path.join("/home/code/style/", req.path_params["file"]))# (f.read(), mimetype="text/css")


@app.route("/edit/{note}")
async def edit(req):
    note = req.path_params["note"]
    return templates.TemplateResponse("edit.html", {
        "request": req,
        "noteID": note
    })


@app.route("/view/{note}")
async def view(req):
    q = note.select()#.where(note.note_id == req.path_params["note"])
    id,filePath,name = await database.fetch_one(q)

    with open(os.path.join("files", filePath)) as f:
        content = f.read()

    return templates.TemplateResponse("view.html", {
        "request": req,
        "content": content
    })


@app.route("/newNote")
async def new_note(req):
    location = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

    await database.execute(note.insert(), values={
        "file_name": str(uuid.uuid4()),
        "note_id": location
    })



    #user = Note.create(file_name=str(uuid.UUID()), note_id=location)

    #print(f"User({user.note_id}:{user.file_name})")

    return RedirectResponse(f"/edit/{location}")


@app.route("/saveNote/{note}", methods=["POST"])
async def save_note(req):
    # Get the file path for this note
    jsonData = await req.json()

    q = note.select()#.where(note.note_id == req.path_params["note"])
    id,filePath,name = await database.fetch_one(q)

    with open(os.path.join("files", filePath), "w") as f:
        f.write(jsonData["content"])

    return JSONResponse({
        "Status": 1
    })


#
#
# @app.route("/saveNote/<note>")
# def saveNote(note):
#     pass
