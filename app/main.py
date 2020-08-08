from starlette.applications import Starlette
from starlette.responses import JSONResponse, RedirectResponse, PlainTextResponse, Response
from starlette.config import Config
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
import string
import random
import uuid
from databases import Database
from urllib.parse import unquote
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter
from hashlib import md5

from app.authentication.Authenticator import UKAuthAuthenticator, BulkAuthenticator, CookieAuthenticator
from app.storage.NoteStorage import LocalNoteStorage
from app.models.Models import note, view as view_table, metadata

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL")

middleware = [
    Middleware(GZipMiddleware, minimum_size=1000)
]

app = Starlette(debug=DEBUG, middleware=middleware)
templates = Jinja2Templates("templates")
app.mount('/static', StaticFiles(directory='static'))


database = Database(DATABASE_URL)

storageBackend = LocalNoteStorage()
authenticator = BulkAuthenticator([UKAuthAuthenticator(), CookieAuthenticator()])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.route("/")
async def root(req):
    claims = await authenticator.get_auth_claims(req)

    #TODO: .order_by()
    public_notes = await database.fetch_all(note.select().where(note.c.public == True).limit(10))

    public_and_views = [(pub_note, (await database.fetch_one(view_table.select().where(view_table.c.note_id == pub_note.id).alias("tmp").count()))[0]) for pub_note in public_notes]

    if claims:
        user_notes = await database.fetch_all(note.select().where(note.c.owner == claims["userId"]))
        return templates.TemplateResponse("main.html", {"request": req, "user": claims, "notes": user_notes, "public_notes": public_and_views})
    else:
        previous_notes = [x[0].split("_")[0] for x in filter(lambda x: "_securityKey" in x[0], req.cookies.items())]
        previous_notes_old = [(await database.fetch_one(note.select().where(note.c.note_id == note_id))) for note_id in previous_notes]

        if previous_notes_old:
            return templates.TemplateResponse("main.html", {"request": req, "user": None, "notes": previous_notes_old, "public_notes": public_and_views})
        else:
            # User not logged in so redirect to new note
            location = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))

            security_key = str(uuid.uuid4())

            await database.execute(note.insert(), values={
                "file_name": str(uuid.uuid4()),
                "note_id": location,
                "security_key": security_key,
                "owner": -1 if claims is None else claims["userId"]
            })

            resp = templates.TemplateResponse("edit.html", {
                "request": req,
                "noteID": location,
                "content": "",
                "user": claims
            })
            resp.set_cookie(f"{location}_securityKey", security_key)

            return resp


@app.route("/edit/{note}")
async def edit(req):
    claims = await authenticator.get_auth_claims(req)

    db_note = await database.fetch_one(note.select().where(note.c.note_id == req.path_params["note"]))

    if db_note is None:
        return RedirectResponse("/")

    if not await authenticator.can_access_resource(req, db_note):
        return RedirectResponse(f"/view/{db_note.note_id}")

    content = await storageBackend.get(db_note.file_name)

    return templates.TemplateResponse("edit.html", {
        "request": req,
        "noteID": db_note.note_id,
        "content": content,
        "user": claims
    })


@app.route("/view/{note}")
async def view(req):

    ip = req.client.host
    try:
        ip = req.headers['HTTP_X_FORWARDED_FOR']
    except KeyError as e:
        print("Not behind a proxy")
    ip_hashed = md5(ip.encode("UTF-8")).hexdigest()
    print(ip_hashed)

    db_note = await database.fetch_one(note.select().where(note.c.note_id == req.path_params["note"]))

    if db_note is None:
        return RedirectResponse("/")

    await database.execute(view_table.insert(), values={
        "note_id": db_note.id,
        "visitor_id": ip_hashed,
    })

    content_raw = await storageBackend.get(db_note.file_name)
    content = highlight(content_raw, guess_lexer(content_raw), HtmlFormatter())

    view_count = await database.fetch_one(view_table.select().where(view_table.c.note_id == db_note.id).alias("tmp").count())

    return templates.TemplateResponse("view.html", {
        "request": req,
        "content": content,
        "contentRaw": content_raw,
        "noteID": db_note.note_id,
        "view_count": view_count[0],
        "user": await authenticator.get_auth_claims(req)
    })


@app.route("/view/{note}/raw")
async def view_raw(req):
    db_note = await database.fetch_one(note.select().where(note.c.note_id == req.path_params["note"]))

    if db_note is None:
        return RedirectResponse("/")

    content = await storageBackend.get(db_note.file_name)

    if not content:
        return RedirectResponse("/")

    return PlainTextResponse(content, media_type="text/plain")


@app.route("/view/{note}/embed")
async def view_oembed(req):
    noteID = req.path_params["note"]

    db_note = await database.fetch_one(note.select().where(note.c.note_id == noteID))

    content = await storageBackend.get(db_note.file_name)

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
    claims = await authenticator.get_auth_claims(req)

    location = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
    security_key = str(uuid.uuid4())
    file_name = str(uuid.uuid4())

    await database.execute(note.insert(), values={
        "file_name": file_name,
        "note_id": location,
        "security_key": security_key,
        "owner": -1 if claims is None else claims["userId"]
    })

    await storageBackend.set(file_name, "")

    resp = RedirectResponse(f"/edit/{location}")
    resp.set_cookie(f"{location}_securityKey", security_key)
    return resp


# Consider using a websocket in future
@app.route("/saveNote/{note}", methods=["POST"])
async def save_note(req):
    # Get the file path for this note
    json_data = await req.json()

    db_note = await database.fetch_one(note.select().where(note.c.note_id == req.path_params["note"]))

    if not await authenticator.can_access_resource(req, db_note):
        return Response(status_code=403)

    await storageBackend.set(db_note.file_name, unquote(json_data["content"]))

    return JSONResponse({
        "Status": 1
    })


@app.route("/note/{id}/set-public")
async def set_note_public(req):
    db_note = await database.fetch_one(note.select().where(note.c.note_id == req.path_params["id"]))

    if not await authenticator.can_access_resource(req, db_note):
        return Response(status_code=403)

    await database.execute(note.update().where(note.c.note_id == req.path_params["id"]).values(public=True))

    return Response(status_code=200)


@app.route("/clone/{note}", methods=["POST"])
async def save_note(req):
    claims = await authenticator.get_auth_claims(req)

    location = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
    security_key = str(uuid.uuid4())
    file_name = str(uuid.uuid4())

    await database.execute(note.insert(), values={
        "file_name": file_name,
        "note_id": location,
        "security_key": security_key,
        "owner": -1 if claims is None else claims["userId"]
    })

    original_note = await database.fetch_one(note.select().where(note.c.note_id == req.path_params["note"]))
    original_content = await storageBackend.get(original_note.file_name)
    await storageBackend.set(file_name, original_content)

    resp = PlainTextResponse(location)
    resp.set_cookie(f"{location}_securityKey", security_key)
    return resp
