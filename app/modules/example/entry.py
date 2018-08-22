from re import compile as regex
from jinja2 import TemplateNotFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import MultipleResultsFound
from flask import (
    Blueprint, 
    Response, 
    render_template, 
    abort, 
    request, 
    url_for, 
    redirect
)

from app import app, db, model

example_bp = Blueprint(
    "example", 
    __name__, 
    template_folder="templates",
    static_folder="assets"
)

@example_bp.route("/")
def index():
    kwargs = dict()
    return render_template("example.html", **kwargs)

@example_bp.route("/<page>")
def dynamic(page):
    kwargs = dict()
    charset = regex(r"^[a-zA-Z0-9_-]+$")

    if not charset.match(page):
        abort(Response("Page does not exist", 404))
        return

    try:
        return render_template("%s.html" % page, **kwargs)
    except TemplateNotFound:
        abort(Response("Page does not exist", 404))