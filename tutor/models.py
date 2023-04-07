from datetime import datetime
from . import db


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)

    announcements = db.relationship('Announcement', backref='subject', lazy=True)

    def __repr__(self):
        return f"Subject('{self.id}', '{self.type}')"


class Localisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    localisation = db.Column(db.String(30), nullable=False)

    announcements = db.relationship('Announcement', backref='location', lazy=True)

    def __repr__(self):
        return f"Localisation('{self.id}', '{self.localisation}')"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(9), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False, default="")

    announcements = db.relationship('Announcement', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}')"


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    is_negotiable = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    localisation_id = db.Column(db.Integer, db.ForeignKey('localisation.id'), nullable=False)

    def __repr__(self):
        return f"Announcement('{self.id}', '{self.title}', '{self.date_posted}')"
