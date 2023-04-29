import base64
from PIL import Image
from io import BytesIO

from flask import jsonify, request

from tutor import app, session, response, bcrypt
from tutor.database import get_user_by_id, get_user_by_username, commit_database, delete_from_database, check_email, \
    check_phone
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

    # Checking if email is valid
    if not check_email(data['email']):
        return response.CONFLICT

    # Checking if phone number is valid or null
    if data['phone'] is not None:
        if not check_phone(data['phone']):
            return response.CONFLICT

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


@app.route("/my_account/password", methods=["PUT"])
def change_password():
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    data = request.get_json(force=True)

    # Checking input data
    if 'old_password' not in data or 'new_password' not in data:
        return response.BAD_REQUEST

    # old password is not correct
    if not bcrypt.check_password_hash(user.password, data['old_password']):
        return response.CONFLICT

    hashed_new_password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')

    user.password = hashed_new_password
    commit_database()

    # Logout
    session.pop('user_id', None)

    return response.SUCCESS


@app.route("/user/<username>", methods=["GET"])
def user_info(username: str):
    user = get_user_by_username(username)

    if user is None:
        return response.BAD_REQUEST

    return jsonify(get_user_data(user))


@app.route("/user/<username>/avatar", methods=["GET"])
def avatar(username: str):
    user = get_user_by_username(username)

    if user is None:
        return response.BAD_REQUEST

    if user.image_file is None:
        return jsonify(None)

    avatar_img = user.image_file
    avatar_base64 = base64.b64encode(avatar_img).decode("utf-8")

    return jsonify(avatar_base64)


@app.route("/my_account/avatar", methods=["GET", "DELETE", "PUT"])
def my_avatar():
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    if request.method == 'GET':

        if user.image_file is None:
            return jsonify(None)

        avatar_img = user.image_file
        avatar_base64 = base64.b64encode(avatar_img).decode("utf-8")

        return jsonify(avatar_base64)

    if request.method == 'DELETE':
        user.image_file = None
        commit_database()
        return response.SUCCESS

    if 'file' not in request.files:
        return response.BAD_REQUEST

    pic = request.files['file']

    if not pic:
        return response.BAD_REQUEST

    pic_stream = pic.stream.read()

    # Check image size
    pil_img = Image.open(BytesIO(pic_stream))

    if pil_img.size[0] > 512 or pil_img.size[1] > 512:
        return response.BAD_REQUEST

    # Check image type
    if pil_img.format not in ["PNG", "JPEG"]:
        return response.BAD_REQUEST

    # PUT
    user.image_file = pic_stream
    commit_database()
    return response.SUCCESS
