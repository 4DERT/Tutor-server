from flask import jsonify, request

from tutor import app, session, response
from tutor.database import get_user_by_id, get_user_by_username, commit_database, delete_from_database
from tutor.models import DegreeCourse
from tutor.serialize import get_user_data


@app.route("/my_account", methods=["GET", "DELETE", "PUT"])
def dashboard():
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    if request.method == 'GET':
        return jsonify(get_user_data(user))

    if request.method == 'DELETE':
        # logout
        session.pop('user_id', None)

        # deleting reviews
        for review in user.reviews_given:
            delete_from_database(review, to_commit=False)

        for review in user.reviews_received:
            delete_from_database(review, to_commit=False)

        # deleting announcements
        for announcement in user.announcements:
            delete_from_database(announcement, to_commit=False)

        delete_from_database(user, True)
        return response.SUCCESS

    # PUT method

    # Checking input data
    data = request.get_json(force=True)

    conditions = [
        'email' not in data,
        'name' not in data,
        'surname' not in data,
        'phone' not in data,
        'description' not in data,
        'degree_course' not in data,
        'semester' not in data,
    ]
    if any(conditions):
        return response.BAD_REQUEST

    # Checking if degree_course exists
    degree_course = DegreeCourse.query.filter_by(degree_course=data['degree_course']).first()
    if degree_course is None:
        return response.CONFLICT

    # Checking if semester exists
    if data['semester'] < 0 or data['semester'] > 7:
        return response.CONFLICT

    # Updating account
    user.email = data['email']
    user.name = data['name']
    user.surname = data['surname']
    user.phone = data['phone']
    user.description = data['description']
    user.degree_course_id = degree_course.id
    user.semester = data['semester']

    commit_database()
    return response.SUCCESS


@app.route("/user/<username>", methods=["GET"])
def user_info(username: str):
    user = get_user_by_username(username)

    if user is None:
        return response.BAD_REQUEST

    return jsonify(get_user_data(user))