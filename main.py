#!env/bin/python3

import hashlib
from os import urandom
from os.path import isfile, realpath, dirname
from app import app, manager

def sha256(seed=None):
    m = hashlib.sha256()
    if seed is not None:
        m.update(seed.encode("utf-8"))
    else:
        m.update(urandom(32))
    return m.hexdigest()

if __name__ == "__main__":
    if manager is not None:
        manager.run()

    path = dirname(realpath(__file__))
    secret = "%s/app/app.secret" % path
    if not isfile(secret):
        with open(secret, "w") as f:
            f.write(sha256())

    app.run(debug=True, host="127.0.0.1", port=10201)