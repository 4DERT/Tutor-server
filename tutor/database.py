from . import db, bcrypt
from .models import Announcement, Subject, User
import re


def init_subjects():
    subjects = [
        "matematyka",
        "fizyka",
        "biologia",
        "przyroda",
        "informatyka",
        "chemia"
    ]

    if db.session.query(Subject).count() == len(subjects):
        return

    for subject in subjects:
        sub = Subject(subject=subject)
        db.session.add(sub)

    db.session.commit()


def create_db():
    db.create_all()
    init_subjects()


def insert_announcement(announcement: Announcement):
    db.session.add(announcement)
    db.session.commit()


def insert_user(user: User):
    db.session.add(user)
    db.session.commit()


def get_user(username_or_email: str, password: str) -> User | None:
    if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', username_or_email):
        user = db.session.query(User).filter(User.email == username_or_email).first()
    else:
        user = db.session.query(User).filter(User.username == username_or_email).first()

    if user is None:
        return None

    if bcrypt.check_password_hash(user.password, password):
        return user

    return None


def get_user_by_id(user_id: int) -> User | None:
    user = db.session.query(User).filter(User.id == user_id).first()
    return user


def get_user_by_username(username: str) -> User:
    return db.session.query(User).filter(User.username == username).first()