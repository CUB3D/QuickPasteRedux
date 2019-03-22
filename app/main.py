from flask import Flask, render_template, redirect, Response, url_for
import os
import string
import random

app = Flask(__name__, template_folder="../templates")


@app.route("/")
def root():
    return render_template("main.html")


@app.route("/resource/<file>")
def resource(file):
    f = open(os.path.join("/home/code/style/", file))
    return Response(f.read(), mimetype="text/css")


@app.route("/edit/<note>")
def edit(note):
    return render_template("edit.html")


@app.route("/newNote")
def newNote():
    location = "".join([random.choice(string.ascii_lowercase) for x in range(7)])
    return redirect(url_for("edit", note=location))

@app.route("/saveNote/<note>")
def saveNote(note):
    pass

app.run(host="0.0.0.0", port=8080)
