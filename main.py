from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Subject('{self.id}', '{self.subject}')"


class Localisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    localisation = db.Column(db.String(30), nullable=False)

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


def test_db():
    regions = [
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

    subjects = [
        "matematyka",
        "fizyka",
        "biologia",
        "wf"
    ]

    db.create_all()

    for region in regions:
        loc = Localisation(localisation=region)
        db.session.add(loc)
    # db.session.commit()

    for subject in subjects:
        sub = Subject(subject=subject)
        db.session.add(sub)
    db.session.commit()

    print(Subject.query.get(1))

    user_1 = User(username="4DERT", email="4dert@demo.com", password="passwd", name="K", surname="D", phone="213742069")
    user_2 = User(username="Corn", email="corn@demo.com", password="passwd", name="Corey", surname="Tey",
                  phone="213742067")
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()
    print("Users:")
    print(User.query.all())

    announcement_1 = Announcement(title="Biologia do matury",
                                  content="Szybka nauka do matury",
                                  user_id=user_1.id,
                                  price=30,
                                  is_negotiable=True,
                                  subject_id=Subject.query.get(2).id,
                                  localisation_id=Localisation.query.get(2).id)

    announcement_2 = Announcement(title="Matematyka do matury rozszerzonej",
                                  content="skuteczna nauka do matury rozszerzonej",
                                  user_id=user_2.id,
                                  price=30,
                                  is_negotiable=True,
                                  subject_id=Subject.query.get(1).id,
                                  localisation_id=Localisation.query.get(1).id)
    db.session.add(announcement_1)
    db.session.add(announcement_2)
    db.session.commit()
    print("Announcements:")
    print(Announcement.query.all())

    print("User_1 announcements:")
    u = User.query.get(1)
    print(u.announcements)  # should be empty

    print("Announcement_2 author:")
    print(announcement_2.author)

    db.drop_all()


if __name__ == '__main__':
    test_db()
