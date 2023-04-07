from . import db
from .models import Announcement, Location, Subject, User


def init_localisations():
    locations = [
        "dolnośląskie",
        "kujawsko-pomorskie",
        "lubelskie",
        "lubuskie",
        "łódzkie",
        "małopolskie",
        "mazowieckie",
        "opolskie",
        "podkarpackie",
        "podlaskie",
        "pomorskie",
        "śląskie",
        "świętokrzyskie",
        "warmińsko-mazurskie",
        "wielkopolskie",
        "zachodniopomorskie",
    ]

    if db.session.query(Location).count() == len(locations):
        return

    for l in locations:
        loc = Location(location=l)
        db.session.add(loc)

    db.session.commit()


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
    init_localisations()
    init_subjects()


def insert_announcement(announcement: Announcement):
    db.session.add(announcement)
    db.session.commit()


def insert_user(user: User):
    db.session.add(user)
    db.session.commit()
