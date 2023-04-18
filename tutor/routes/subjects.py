from flask import jsonify, request

from tutor import app, session, ADMINS, response
from tutor.database import get_user_by_id, get_degree_course, \
    get_subject, insert_into_database
from tutor.models import Subject
from tutor.serialize import get_subjects


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


@app.route("/subjects", methods=["GET"])
def subjects():
    return jsonify(get_subjects())