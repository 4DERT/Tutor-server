from .models import Announcement, Localisation, Subject, User


def get_announcements():
    announcements = []

    for obj in Announcement.query.all():
        announcements.append(
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
                'location': obj.location.localisation
            }
        )

    return announcements

