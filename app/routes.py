from flask import render_template, session, make_response, request

from app import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/")