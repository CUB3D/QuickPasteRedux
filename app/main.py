from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse, RedirectResponse, PlainTextResponse
from starlette.config import Config
from starlette.templating import Jinja2Templates
from starlette.routing import Mount, Route, Router
from starlette.staticfiles import StaticFiles
import os
import string
import random
import uuid
from databases import Database
from urllib.parse import unquote
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter
from sqlalchemy import Table, Column, Integer, String
import sqlalchemy

config = Config(os.environ["STARTLETTE_CONFIG"])
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL")

app = Starlette(debug=DEBUG)
templates = Jinja2Templates("templates")
app.mount('/static', StaticFiles(directory='static'))


database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

note = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("file_name", String(length=255)),
    Column("note_id", String(length=255)),
    Column("security_key", String(length=255))
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


@app.route("/edit/{note}")
async def edit(req):
    noteID = req.path_params["note"]

    q = note.select().where(note.c.note_id == noteID)
    id, filePath, name, securityKey = await database.fetch_one(q)

    # Make sure the user can edit this file
    if securityKey != req.cookies.get(f"{noteID}_securityKey"):
        return RedirectResponse(f"/view/{noteID}")

    filePath = os.path.join("files", filePath)

    if os.path.exists(filePath):
        with open(filePath) as f:
            content = f.read()
    else:
        content = ""

    return templates.TemplateResponse("edit.html", {
        "request": req,
        "noteID": noteID,
        "content": content
    })


@app.route("/view/{note}")
async def view(req):
    noteID = req.path_params["note"]

    q = note.select().where(note.c.note_id == noteID)
    id, filePath, name, securityKey = await database.fetch_one(q)

    filePath = os.path.join("files", filePath)

    if os.path.exists(filePath):
        with open(filePath) as f:
            content = f.read()
    else:
        return RedirectResponse("/")

    content = highlight(content, guess_lexer(content), HtmlFormatter())

    return templates.TemplateResponse("view.html", {
        "request": req,
        "content": content,
        "noteID": noteID
    })


@app.route("/view/{note}/raw")
async def view_raw(req):
    noteID = req.path_params["note"]

    q = note.select().where(note.c.note_id == noteID)
    id, filePath, name, securityKey = await database.fetch_one(q)

    filePath = os.path.join("files", filePath)

    if os.path.exists(filePath):
        with open(filePath) as f:
            content = f.read()
    else:
        return RedirectResponse("/")

    return PlainTextResponse(content, media_type="text/plain")


@app.route("/view/{note}/embed")
async def view_raw(req):
    noteID = req.path_params["note"]

    q = note.select().where(note.c.note_id == noteID)
    id, filePath, name, securityKey = await database.fetch_one(q)

    filePath = os.path.join("files", filePath)

    if os.path.exists(filePath):
        with open(filePath) as f:
            content = f.read()
    else:
        return RedirectResponse("/")

    content = highlight(content, guess_lexer(content), HtmlFormatter())

    return JSONResponse({
        "version": "1.0",
        "type": "rich",
        "title": noteID,
        "width": 200,
        "height": 200,
        "html": content[:250]
    })


@app.route("/pygmentStyle")
async def style(req):
    return PlainTextResponse(HtmlFormatter().get_style_defs("#editor-pane"), media_type="text/css")


@app.route("/newNote")
async def new_note(req):
    location = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
    securityKey = str(uuid.uuid4())

    await database.execute(note.insert(), values={
        "file_name": str(uuid.uuid4()),
        "note_id": location,
        "security_key": securityKey
    })

    resp = RedirectResponse(f"/edit/{location}")
    resp.set_cookie(f"{location}_securityKey", securityKey)
    return resp


@app.route("/saveNote/{note}", methods=["POST"])
async def save_note(req):
    # Get the file path for this note
    jsonData = await req.json()

    q = note.select().where(note.c.note_id == req.path_params["note"])
    id, filePath, name, sk = await database.fetch_one(q)

    with open(os.path.join("files", filePath), "w") as f:
        f.write(unquote(jsonData["content"]))

    return JSONResponse({
        "Status": 1
    })
