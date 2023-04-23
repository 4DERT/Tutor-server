from typing import Dict, Any, List

import sqlalchemy
from .models import Announcement, Subject, User, DegreeCourse
from .database import get_degree_course_by_id, get_degree_course, get_user_by_id


def get_announcements(price_from: int | None = None,
                      price_to: int | None = None,
                      subject: str | None = None,
                      degree_course: str | None = None,
                      semester: int | None = None,
                      is_negotiable: bool | None = None,
                      date_posted_from: str | None = None,
                      date_posted_to: str | None = None,
                      announcement_id: int | None = None,
                      price_sort: str | None = None,
                      date_sort: str | None = None):
    # Subject filtering
    dg = get_degree_course(degree_course)
    subject_filters_by = {
        "subject": subject,
        "degree_course_id": dg.id if dg is not None else None,
        "semester": semester
    }
    subject_final_filters_by = {key: val for key, val in subject_filters_by.items() if val is not None}
    subjects = Subject.query.filter_by(**subject_final_filters_by) if len(subject_final_filters_by) != 0 else []

    # Announcements filtering
    filters = [
        (Announcement.is_negotiable == is_negotiable) if is_negotiable else None,
        (Announcement.price >= price_from) if price_from else None,
        (Announcement.price <= price_to) if price_to else None,
        (Announcement.date_posted >= date_posted_from) if date_posted_from else None,
        (Announcement.date_posted <= date_posted_to) if date_posted_to else None,
        (Announcement.id == announcement_id) if announcement_id else None,
    ]
    filters_or = [(Announcement.subject_id == s.id) for s in subjects]
    final_filters = [f for f in filters if f is not None]

    # Announcements sorting
    sort = [
        (Announcement.price.asc()) if price_sort == 'asc' else None,
        (Announcement.price.desc()) if price_sort == 'desc' else None,
        (Announcement.date_posted.asc()) if date_sort == 'asc' else None,
        (Announcement.date_posted.desc()) if date_sort == 'desc' else None
    ]
    final_sort = [s for s in sort if s is not None]

    query = Announcement.query.filter(*final_filters, sqlalchemy.or_(*filters_or)).order_by(*final_sort)

    return [
        {
            'id': obj.id,
            'title': obj.title,
            'date_posted': obj.date_posted.strftime("%Y-%m-%d"),
            'content': obj.content,
            'price': obj.price,
            'is_negotiable': obj.is_negotiable,
            'announcer_username': obj.author.username,
            'announcer_name': obj.author.name,
            'announcer_surname': obj.author.surname,
            'announcer_email': obj.author.email,
            'announcer_phone': obj.author.phone,
            'subject': obj.subject.subject,
            'degree_course': obj.subject.degree_course.degree_course,
            'semester': obj.subject.semester

        } for obj in query
    ]


def get_user_data(user: User):
    return {
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "phone": user.phone,
        "description": user.description,
        "announcements": [{
            'id': obj.id,
            'title': obj.title,
            'date_posted': obj.date_posted,
            'content': obj.content,
            'price': obj.price,
            'is_negotiable': obj.is_negotiable,
            'subject': obj.subject.subject,
        } for obj in user.announcements],
        "reviews": [{
            "rate": rev.rate,
            "review": rev.review,
            "reviewer": get_user_by_id(rev.reviewer_id).username,
            "date": rev.date
        } for rev in user.reviews_received]
    }


def get_subjects():
    return [{
        "subject": s.subject,
        "degree_course": get_degree_course_by_id(s.degree_course_id).degree_course,
        "semester": s.semester
        } for s in Subject.query.all()]


def get_subject_detail(subject_id: int):
    subject = Subject.query.filter(Subject.id == subject_id).first()
    return {
        "subject": subject.subject,
        "degree_course": get_degree_course_by_id(subject.degree_course_id).degree_course,
        "semester": subject.semester,
        "announcements": [a.announcements for a in subject.announcements]
    }


def get_degree_courses():
    return [dg.degree_course for dg in DegreeCourse.query.all()]


def get_degree_course_details(dg_id: int) -> dict[str, list[Any] | Any] | None:
    dg = DegreeCourse.query.filter(DegreeCourse.id == dg_id).first()
    return {
        "degree_course": dg.degree_course,
        "subjects": [s.subject for s in dg.subjects],
        "users": [u.username for u in dg.users]
    }
