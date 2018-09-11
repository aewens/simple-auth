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
    uuid = request.form.get("uuid")
    user = models.User.query.filter_by(uuid=uuid).one_or_none()

    if user is None:
        return send(1, "User does not exist")

    token = models.Token(value=sha256(), user=user)
    db.session.add(token)
    db.session.commit()

    return send(0, token.value)

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
    permissions = token.permissions
    expires = token.expires_at

    if expires > 0:
        expires = expires + timestamp()

    info = ";".join([uuid, str(permissions), str(expires)])
    signature = sign(info, app.secret_key).replace("+", "!")

    return send(0, ",".join([
        info,
        signature
    ]))

@app.route("/verify", methods=["POST"])
def verify():
    voucher = request.form.get("voucher")
    print(voucher)

    if "," not in voucher:
        return send(1, "Invalid format for voucher")

    info, signature = voucher.split(",")
    signature = signature.replace("!", "+")
    signed = sign(info, app.secret_key)
    if signed != signature:
        print(signed, signature, info)
        return send(2, "Signature doesn't match content")

    if ";" not in info:
        return send(3, "Invalid format for voucher information")

    uuid, permissions, expires = info.split(";")
    user = models.User.query.filter_by(uuid=uuid).one_or_none()
    
    if user is None:
        return send(4, "User doesn't exist")

    if int(permissions) < 0:
        return send(5, "User lacks valid permissions")

    exp = int(expires)
    if exp > 0 and timestamp() > exp:
        return send(6, "Voucher has expired")

    return send(0, "Verified")