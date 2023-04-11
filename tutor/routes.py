from . import app, bcrypt, session
from .database import insert_announcement, insert_user, get_user, get_user_by_id, get_user_by_username
from .models import Announcement, User, Subject, Location
from flask import jsonify, request, abort
from .serialize import get_announcements, get_locations, get_user_data


@app.route("/", methods=["GET"])
def home():
    return jsonify(get_announcements())


@app.route("/locations", methods=["GET"])
def locations():
    return jsonify(get_locations())


@app.route("/new_announcement", methods=["POST"])
def new_announcement():
    data = request.get_json(force=True)

    if 'user_id' not in session:
        return abort(400)

    user_id = session['user_id']

    try:
        announcement = Announcement(
            title=data['title'],
            content=data['content'],
            price=data['price'],
            is_negotiable=data['is_negotiable'],
            user_id= user_id,
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


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)

    username_or_email = data['user']
    password = data['password']

    user = get_user(username_or_email, password)
    if user is not None:

        # Logout current user
        if 'user_id' in session:
            session.pop('user_id', None)

        session['user_id'] = user.id
        return "ok"

    return abort(400, "Incorrect username or password")


@app.route("/logout", methods=["GET"])
def logout():
    session.pop('user_id', None)
    return "ok"


@app.route("/my_account", methods=["GET"])
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        user = get_user_by_id(user_id)

        return jsonify(get_user_data(user))
    else:
        abort(400, "User not logged")


@app.route("/user/<username>", methods=["GET"])
def user_info(username: str):
    user = get_user_by_username(username)

    if user is not None:
        return jsonify(get_user_data(user))
