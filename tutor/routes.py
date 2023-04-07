from . import app
from flask import jsonify

from .serialize import get_announcements


@app.route("/", methods=["GET"])
def home():
    return jsonify(get_announcements())
