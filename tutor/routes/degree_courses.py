from flask import jsonify, request

from tutor import app, session, ADMINS, response
from tutor.database import get_user_by_id, get_degree_course, \
    insert_into_database, get_degree_course_by_id, delete_from_database, commit_database
from tutor.models import DegreeCourse
from tutor.serialize import get_degree_courses, get_degree_course_details


@app.route("/degree_courses", methods=["GET", "POST"])
def degree_courses():

    if request.method == 'GET':
        return jsonify(get_degree_courses())

    # POST method
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


@app.route("/degree_courses/<dg_name>", methods=["GET", "PUT", "DELETE"])
def degree_course_detail(dg_name: str):

    # Check if degree course exists
    dg = get_degree_course(dg_name)
    if dg is None:
        return response.BAD_REQUEST

    if request.method == 'GET':
        return jsonify(get_degree_course_details(dg.id))

    # Checking if user is logged
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    # Checking if user is an admin
    if user.username not in ADMINS:
        return response.FORBIDDEN

    if request.method == 'DELETE':
        # remove subjects
        for s in dg.subjects:

            # remove announcements
            for a in s.announcements:
                delete_from_database(a, False)

            delete_from_database(s, False)

        delete_from_database(dg, False)
        commit_database()

        return response.SUCCESS

    # PUT method

    # Checking input data
    data = request.get_json(force=True)

    if 'degree_course' not in data:
        return response.CONFLICT

    dg.degree_course = data['degree_course']
    commit_database()
    return response.SUCCESS
