# Packages
from sys import argv, exit
from os.path import realpath, dirname
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

# Local
from config import Config

path = dirname(realpath(__file__))
secret = "%s/app/app.secret" % path
if not isfile(secret):
    print("Error: Missing file '%s'" % secret)
    exit(1)

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