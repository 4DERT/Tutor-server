from flask import jsonify, request

from tutor import app, session, ADMINS, response
from tutor.database import get_user_by_id, get_degree_course, \
    insert_into_database
from tutor.models import DegreeCourse
from tutor.serialize import get_degree_courses


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


@app.route("/degree_courses", methods=["GET"])
def degree_courses():
    return jsonify(get_degree_courses())
