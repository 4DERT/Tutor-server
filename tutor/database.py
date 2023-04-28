from . import db, bcrypt
from .models import Announcement, User, DegreeCourse, Subject, Review
import re


def create_db():
    db.create_all()


def insert_into_database(obj: Announcement | User | Subject | DegreeCourse | Review) -> None:
    db.session.add(obj)
    db.session.commit()


def delete_from_database(obj: Announcement | User | Subject | DegreeCourse | Review, to_commit: bool = True) -> None:
    db.session.delete(obj)
    if to_commit:
        db.session.commit()


def get_user(username_or_email: str, password: str) -> User | None:
    if check_email(username_or_email):
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


def get_subject(subject: str, degree_course: str, semester: int) -> Subject | None:
    return db.session.query(Subject).filter(Subject.subject == subject,
                                            Subject.semester == semester,
                                            Subject.degree_course_id == get_degree_course(degree_course).id).first()


def get_announcement_by_id(announcement_id: int) -> Announcement | None:
    return db.session.query(Announcement).filter(Announcement.id == announcement_id).first()


def commit_database() -> None:
    db.session.commit()


def get_review(reviewee: User, reviewer_id: int) -> Review | None:
    for rev in reviewee.reviews_received:
        if rev.reviewer_id == reviewer_id:
            return rev

    return None


def check_email(email: str) -> bool:
    if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
        return True

    return False


def check_phone(phone_number: str) -> bool:
    if re.fullmatch(r'^\d{9}$', phone_number):
        return True

    return False
