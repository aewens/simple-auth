# Packages
from sys import argv
from os.path import isfile, realpath, dirname
from helper import sha256
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

# Local
from config import Config

path = dirname(realpath(__file__))
secret = "%s/app.secret" % path
if not isfile(secret):
    with open(secret, "w") as f:
        f.write(sha256())

app = Flask(__name__, static_url_path="/assets")

with open(secret, "r") as f:
    app.secret_key = f.read()

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = None
if len(argv) > 1:
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)

from app import routes, models