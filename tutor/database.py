from . import models, db


def init_localisations():
    localisations = [
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

    for localisation in localisations:
        loc = models.Localisation(localisation=localisation)
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

    for subject in subjects:
        sub = models.Subject(subject=subject)
        db.session.add(sub)

    db.session.commit()


def create_db():
    db.create_all()
    init_localisations()
    init_subjects()
