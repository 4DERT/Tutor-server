from flask import jsonify, request

from . import app, bcrypt, session, ADMINS, response
from .database import get_user, get_user_by_id, get_user_by_username, get_degree_course, \
    get_subject, insert_into_database
from .models import Announcement, User, Subject, DegreeCourse, Review
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

    # Checking input data
    conditions = [
        'title' not in data,
        'content' not in data,
        'price' not in data,
        'is_negotiable' not in data,
        'degree_course' not in data,
        'subject' not in data,
        'semester' not in data,
    ]
    if any(conditions):
        return response.BAD_REQUEST

    # Checking if user is logged
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']

    # Checking if degree_course exists
    degree_course = DegreeCourse.query.filter_by(degree_course=data['degree_course']).first()
    if degree_course is None:
        return response.CONFLICT

    # Checking if subject exists
    subject = Subject.query.filter_by(subject=data['subject'],
                                      degree_course_id=degree_course.id,
                                      semester=data['semester']).first()
    if subject is None:
        return response.CONFLICT

    # Inserting announcement into db
    announcement = Announcement(
        title=data['title'],
        content=data['content'],
        price=data['price'],
        is_negotiable=data['is_negotiable'],
        user_id=user_id,
        subject_id=subject.id
    )
    insert_into_database(announcement)

    return response.SUCCESS


@app.route("/sign_up", methods=["POST"])
def sign_up():
    data = request.get_json(force=True)

    # Checking input data
    conditions = [
        'username' not in data,
        'email' not in data,
        'password' not in data,
        'name' not in data,
        'surname' not in data,
        'phone' not in data,
    ]
    if any(conditions):
        return response.BAD_REQUEST

    # Checking if user exists
    if get_user(data['username'], data['password']) is not None:
        return response.CONFLICT

    # hashing users password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Inserting user into db
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        name=data['name'],
        surname=data['surname'],
        phone=data['phone']
    )
    insert_into_database(user)

    return response.SUCCESS


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)

    # Checking input data
    if 'user' not in data or 'password' not in data:
        return response.BAD_REQUEST

    username_or_email = data['user']
    password = data['password']

    # Checking if user exists
    user = get_user(username_or_email, password)
    if user is None:
        return response.CONFLICT

    # Logout current user
    if 'user_id' in session:
        session.pop('user_id', None)

    # Add user to session
    session['user_id'] = user.id

    return response.SUCCESS


@app.route("/logout", methods=["GET"])
def logout():
    session.pop('user_id', None)
    return response.SUCCESS


@app.route("/my_account", methods=["GET"])
def dashboard():
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    return jsonify(get_user_data(user))


@app.route("/user/<username>", methods=["GET"])
def user_info(username: str):
    user = get_user_by_username(username)

    if user is None:
        return response.BAD_REQUEST

    return jsonify(get_user_data(user))


@app.route("/new_degree_course", methods=["POST"])
def new_degree_course():
    data = request.get_json(force=True)

    # Checking input data
    if 'degree_course' not in data:
        return response.BAD_REQUEST

    # Checking if user is logged
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    # Checking if user is an admin
    if user.username not in ADMINS:
        return response.FORBIDDEN

    # Checking if degree_course not exists
    degree_course = data['degree_course']
    if get_degree_course(degree_course) is not None:
        return response.CONFLICT

    # Inserting degree_course into database
    insert_into_database(DegreeCourse(degree_course=degree_course))

    return response.SUCCESS


@app.route("/new_subject", methods=["POST"])
def new_subject():
    data = request.get_json(force=True)

    # Checking input data
    conditions = [
        'subject' not in data,
        'degree_course' not in data,
        'semester' not in data,
    ]
    if any(conditions):
        return response.BAD_REQUEST

    # Check if user is logged
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    # Check if user is an admin
    if user.username not in ADMINS:
        return response.FORBIDDEN

    # Checking if degree_course not exists
    degree_course = get_degree_course(data['degree_course'])
    if degree_course is None:
        return response.CONFLICT

    # Checking if degree_course not exists
    subject = get_subject(data['subject'], data['degree_course'], data['semester'])
    if subject is not None:
        return response.CONFLICT

    # Inserting subject into db
    insert_into_database(Subject(subject=data['subject'],
                               degree_course_id=degree_course.id,
                               semester=data['semester']))

    return response.SUCCESS


@app.route("/degree_courses", methods=["GET"])
def degree_courses():
    return jsonify(get_degree_courses())


@app.route("/subjects", methods=["GET"])
def subjects():
    return jsonify(get_subjects())


@app.route("/add_review", methods=["POST"])
def add_review():
    data = request.get_json(force=True)

    # Checking input data
    if 'reviewee' not in data or 'rate' not in data:
        return response.BAD_REQUEST

    reviewee_username = data["reviewee"]
    rate = data["rate"]
    review = data["review"] if "review" in data else None  # review is optional

    if int(rate) < 1 or int(rate) > 5:
        return response.BAD_REQUEST

    # Checking if user is logged
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']

    # Checking if user exists
    reviewee = get_user_by_username(reviewee_username)
    if reviewee is None:
        return response.CONFLICT

    # Check if user already add review to given person
    for revs in reviewee.reviews_received:
        if revs.reviewer_id == user_id:
            return response.CONFLICT

    insert_into_database(
        Review(
            rate=rate,
            review=review,
            reviewer_id=user_id,
            reviewee_id=reviewee.id)
    )

    return response.SUCCESS
