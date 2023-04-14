from . import app, bcrypt, session, ADMINS
from .database import insert_announcement, insert_user, get_user, get_user_by_id, get_user_by_username, get_degree_course, insert_degree_course, get_subject, insert_subject
from .models import Announcement, User, Subject, DegreeCourse
from flask import jsonify, request, abort
from .serialize import get_announcements, get_user_data, get_degree_courses, get_subjects


@app.route("/", methods=["GET"])
def home():

    price_from = request.args.get("price_from")
    price_to = request.args.get("price_to")
    subject = request.args.get("subject")
    degree_course = request.args.get("degree_course")
    semester = request.args.get("semester")
    is_negotiable = request.args.get("is_negotiable")
    date_posted_from = request.args.get("date_posted_from")
    date_posted_to = request.args.get("date_posted_to")

    return jsonify(get_announcements(price_from, price_to, subject, degree_course, semester,
                                     is_negotiable, date_posted_from, date_posted_to))


@app.route("/new_announcement", methods=["POST"])
def new_announcement():
    data = request.get_json(force=True)

    if 'user_id' not in session:
        return abort(400)

    user_id = session['user_id']
    degree_course = DegreeCourse.query.filter_by(degree_course=data['degree_course']).first()

    if degree_course is None:
        return abort(400, "degree_course not exists")

    subject = Subject.query.filter_by(subject=data['subject'],
                                      degree_course_id=degree_course.id,
                                      semester=data['semester']).first()

    if subject is None:
        return abort(400, "subject not exists")

    announcement = Announcement(
        title=data['title'],
        content=data['content'],
        price=data['price'],
        is_negotiable=data['is_negotiable'],
        user_id=user_id,
        subject_id=subject.id
    )

    insert_announcement(announcement)
    return "ok"  # TODO


@app.route("/sign_up", methods=["POST"])
def sign_up():
    data = request.get_json(force=True)

    # Check if user exists
    if get_user(data['username'], data['password']) is not None:
        return abort(400, "User exists")

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


@app.route("/new_degree_course", methods=["POST"])
def new_degree_course():
    data = request.get_json(force=True)

    # Check if user is logged
    if 'user_id' not in session:
        return abort(400, "User not logged")

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    # Check if user is an admin
    if user.username not in ADMINS:
        return abort(400, "User not an admin")

    degree_course = data['degree_course']
    if get_degree_course(degree_course) is None:
        insert_degree_course(DegreeCourse(degree_course=degree_course))
        return "ok"

    return abort(400, "degree_course exists")


@app.route("/new_subject", methods=["POST"])
def new_subject():
    data = request.get_json(force=True)

    # Check if user is logged
    if 'user_id' not in session:
        return abort(400, "User not logged")

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    # Check if user is an admin
    if user.username not in ADMINS:
        return abort(400, "User not an admin")

    degree_course = get_degree_course(data['degree_course'])
    if degree_course is None:
        abort(400, "degree_course not exists")

    subject = get_subject(data['subject'], data['degree_course'], data['semester'])
    if subject is None:
        insert_subject(Subject(subject=data['subject'], degree_course_id=degree_course.id, semester=data['semester']))
        return "ok"

    return abort(400, "subject exists")


@app.route("/degree_courses", methods=["GET"])
def degree_courses():
    return jsonify(get_degree_courses())


@app.route("/subjects", methods=["GET"])
def subjects():
    return jsonify(get_subjects())
