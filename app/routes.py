from flask import render_template, session, make_response, request, jsonify

from helper import sha256
from app import app

def send(status, message):
    return "%s|%s" % (status, message)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate")
def gen():
    return sha256()

@app.route("/auth", methods=["POST"])
def auth():
    value = request.form.get("token")
    token = models.Token.query.filter_by(value=value).one_or_none()

    if token is None:
        status = 1
        message = "Token does not exist"
        return send(status, message)

    status = 0
    message = ",".join([
        token.user.id,
        token.permissions,
        token.created_at,
        token.expires_at,
        token.revoked
    ])

    return send(status, message)