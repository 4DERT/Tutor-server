from . import db, bcrypt
from .models import Announcement, User, DegreeCourse, Subject, Review
import re


def create_db():
    db.create_all()


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


def get_degree_course(degree_course: str) -> DegreeCourse | None:
    return db.session.query(DegreeCourse).filter(DegreeCourse.degree_course == degree_course).first()


def get_degree_course_by_id(id: int) -> DegreeCourse | None:
    return db.session.query(DegreeCourse).filter(DegreeCourse.id == id).first()


def insert_degree_course(degree_course: DegreeCourse):
    db.session.add(degree_course)
    db.session.commit()


def get_subject(subject: str, degree_course: str, semester: int) -> Subject | None:
    return db.session.query(Subject).filter(Subject.subject == subject,
                                            Subject.semester == semester,
                                            Subject.degree_course_id == get_degree_course(degree_course).id).first()


def insert_subject(subject: Subject) -> None:
    db.session.add(subject)
    db.session.commit()


def insert_review(review: Review) -> None:
    db.session.add(review)
    db.session.commit()