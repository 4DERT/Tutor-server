import http.client

import flask

from . import app, db
from .models import Announcement, User, Subject, Location
from flask import jsonify, request

from .serialize import get_announcements, get_locations


@app.route("/", methods=["GET"])
def home():
    return jsonify(get_announcements())


@app.route("/locations", methods=["GET"])
def locations():
    return jsonify(get_locations())


@app.route("/new_announcement", methods=["POST"])
def new_announcement():
    data = request.get_json(force=True)

    try:
        announcement = Announcement(
            title=data['title'],
            content=data['content'],
            price=data['price'],
            is_negotiable=data['is_negotiable'],
            user_id=User.query.filter_by(username=data['announcer_username']).first().id,
            subject_id=Subject.query.filter_by(type=data['subject']).first().id,
            location_id=Location.query.filter_by(location=data['location']).first().id
        )

        db.session.add(announcement)
        db.session.commit()
        return "ok"  # TODO

    except (AttributeError, KeyError) as error:
        return flask.abort(400)
