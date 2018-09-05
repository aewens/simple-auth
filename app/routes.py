from flask import render_template, session, make_response, request, jsonify

from helper import *
from app import app, db, models

def send(status, message):
    return "%s|%s" % (status, message)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new_user")
def new_user():
    user = models.User(uuid=sha256())
    token = models.Token(value=sha256(), user=user)
    db.session.add(token)
    db.session.commit()
    return send(0, token.value)

@app.route("/new_token", methods=["POST"])
def new_token():
    uuid = request.form.get("user")
    return send(0, sha256())

@app.route("/auth", methods=["POST"])
def auth():
    value = request.form.get("token")
    token = models.Token.query.filter_by(value=value).one_or_none()

    if token is None:
        return send(1, "Token does not exist")

    revoked = token.revoked
    if revoked:
        return send(2, "Token has been revoked")

    expires = token.expires_at

    if expires > 0:
        iat = timestamp(token.created_at)
        exp = iat + expires
        now = timestamp()

        if now >= exp:
            return send(3, "Token is expired")

    uuid = token.user.uuid
    signature = sign(uuid, app.secret_key)

    return send(0, ",".join([
        uuid,
        signature
    ]))

@app.route("/verify", methods=["POST"])
def verify():
    return send(0, "")