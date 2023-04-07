from .models import Announcement, Location, Subject, User


def get_announcements():
    return [
        {
            'id': obj.id,
            'title': obj.title,
            'date_posted': obj.date_posted,
            'content': obj.content,
            'price': obj.price,
            'is_negotiable': obj.is_negotiable,
            'announcer_username': obj.author.username,
            'announcer_name': obj.author.name,
            'announcer_surname': obj.author.surname,
            'announcer_email': obj.author.email,
            'announcer_phone': obj.author.phone,
            'subject': obj.subject.type,
            'location': obj.location.location
        } for obj in Announcement.query.all()
    ]


def get_locations():
    return [l.location for l in Location.query.all()]