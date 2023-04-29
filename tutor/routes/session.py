from flask import request

from tutor import app, bcrypt, session, response
from tutor.database import get_user, insert_into_database, check_email, check_phone, get_user_by_email
from tutor.models import User


@app.route("/sign_up", methods=["POST"])
def sign_up():
    data = request.get_json(force=True)

    # Checking input data
    conditions = [
        'username' not in data,
        'email' not in data,
        'password' not in data,
        'name' not in data,
        'surname' not in data
    ]
    if any(conditions):
        return response.BAD_REQUEST

    # Checking if email is valid
    if not check_email(data['email']):
        return response.NOT_VALID_EMAIL

    # Checking if user exists
    if get_user(data['username'], data['password']) is not None:
        return response.EXISTING_USERNAME

    if get_user_by_email(data['email']) is not None:
        return response.EXISTING_EMAIL

    # hashing users password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Inserting user into db
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        name=data['name'],
        surname=data['surname']
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
