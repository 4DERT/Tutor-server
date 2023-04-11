from . import app, bcrypt
from .database import insert_announcement, insert_user
from .models import Announcement, User, Subject, Location
from flask import jsonify, request, abort

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
            subject_id=Subject.query.filter_by(subject=data['subject']).first().id,
            location_id=Location.query.filter_by(location=data['location']).first().id
        )

        insert_announcement(announcement)
        return "ok"  # TODO

    except (AttributeError, KeyError) as error:
        return abort(400)


@app.route("/sign_up", methods=["POST"])
def sign_up():
    data = request.get_json(force=True)

    # TODO: find better validation system
    try:
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            name=data['name'],
            surname=data['surname'],
            phone=data['phone']
        )

        insert_user(user)
        return "ok"  # TODO

    except (AttributeError, KeyError) as error:
        return abort(400)