from flask import render_template

from app import app
from modules.example.entry import example_bp

app.register_blueprint(example_bp, url_prefix="/example")

@app.route("/")
def index():
    return render_template("index.html")