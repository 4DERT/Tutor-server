from .models import Announcement, Subject, User
from . import db


def get_announcements(price_from: int | None,
                      price_to: int | None,
                      subject: str | None,
                      is_negotiable: bool | None,
                      date_posted_from: str | None,
                      date_posted_to: str | None):

    subject_id = Subject.query.filter_by(subject=subject).first().id if subject else None

    # filter_by
    filters_by = {
        "subject_id": subject_id,
        "is_negotiable": is_negotiable,
    }
    final_filters_by = {key: val for key, val in filters_by.items() if val is not None}

    # filter
    filters = [
        (Announcement.price >= price_from) if price_from else None,
        (Announcement.price <= price_to) if price_to else None,
        (Announcement.date_posted >= date_posted_from) if date_posted_from else None,
        (Announcement.date_posted <= date_posted_to) if date_posted_to else None
    ]

    final_filters = [f for f in filters if f is not None]

    query = Announcement.query.filter_by(**final_filters_by).filter(*final_filters)

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
        } for obj in user.announcements]
    }


def get_subjects():
    return [s.subject for s in Subject.query.all()]
