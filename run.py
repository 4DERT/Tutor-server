from tutor import app, db
from tutor.database import create_db
from tutor.serialize import get_announcements
from tutor.models import Announcement, User, Localisation, Subject


def test_db():
    create_db()

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

    print()
    print(get_announcements())

    # db.drop_all()


if __name__ == '__main__':
    # test_db()
    app.run(port=8080, debug=True)
