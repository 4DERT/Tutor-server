from datetime import date
from . import db


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), unique=True, nullable=False)

    announcements = db.relationship('Announcement', backref='subject', lazy=True)

    def __repr__(self):
        return f"Subject('{self.id}', '{self.subject}')"


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(30), unique=True, nullable=False)

    announcements = db.relationship('Announcement', backref='location', lazy=True)

    def __repr__(self):
        return f"Location('{self.id}', '{self.locations}')"


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
    date_posted = db.Column(db.Date, nullable=False, default=date.today())
    content = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    is_negotiable = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)

    def __repr__(self):
        return f"Announcement('{self.id}', '{self.title}', '{self.date_posted}')"
