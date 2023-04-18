from flask import jsonify, request

from tutor import app, session, response
from tutor.database import insert_into_database, get_announcement_by_id, commit_database, delete_from_database
from tutor.models import Announcement, Subject, DegreeCourse
from tutor.serialize import get_announcements


# Showing all announcements
@app.route("/", methods=["GET"])
@app.route("/announcements", methods=["GET"])
def get_all_announcements():
    # filtering
    price_from = request.args.get("price_from")
    price_to = request.args.get("price_to")
    subject = request.args.get("subject")
    degree_course = request.args.get("degree_course")
    semester = request.args.get("semester")
    is_negotiable = request.args.get("is_negotiable")
    date_posted_from = request.args.get("date_posted_from")
    date_posted_to = request.args.get("date_posted_to")

    # sorting
    price_sort = request.args.get("price_sort")
    date_sort = request.args.get("date_sort")

    return jsonify(get_announcements(price_from, price_to, subject, degree_course, semester,
                                     is_negotiable, date_posted_from, date_posted_to, None, price_sort, date_sort))


# Showing single announcement
@app.route("/announcements/<int:announcement_id>", methods=["GET"])
def get_announcement(announcement_id):
    announcements = get_announcements(announcement_id=announcement_id)

    if len(announcements) == 0:
        return response.BAD_REQUEST

    return jsonify(announcements)


# Adding announcement
@app.route("/new_announcement", methods=["POST"])
def new_announcement():
    data = request.get_json(force=True)

    # Checking input data
    conditions = [
        'title' not in data,
        'content' not in data,
        'price' not in data,
        'is_negotiable' not in data,
        'degree_course' not in data,
        'subject' not in data,
        'semester' not in data,
    ]
    if any(conditions):
        return response.BAD_REQUEST

    # Checking if user is logged
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']

    # Checking if degree_course exists
    degree_course = DegreeCourse.query.filter_by(degree_course=data['degree_course']).first()
    if degree_course is None:
        return response.CONFLICT

    # Checking if subject exists
    subject = Subject.query.filter_by(subject=data['subject'],
                                      degree_course_id=degree_course.id,
                                      semester=data['semester']).first()
    if subject is None:
        return response.CONFLICT

    # Inserting announcement into db
    announcement = Announcement(
        title=data['title'],
        content=data['content'],
        price=data['price'],
        is_negotiable=data['is_negotiable'],
        user_id=user_id,
        subject_id=subject.id
    )
    insert_into_database(announcement)

    return response.SUCCESS


# Updating announcement
@app.route("/announcements/<int:announcement_id>", methods=["PUT", "DELETE"])
def update_announcement(announcement_id):
    announcement = get_announcement_by_id(announcement_id)

    # Checking if announcement exists
    if announcement is None:
        return response.BAD_REQUEST

    # Checking if user is logged
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']

    # Checking if user edits own announcement
    if announcement.user_id != user_id:
        return response.UNAUTHORIZED

    if request.method == 'DELETE':
        delete_from_database(announcement)
        return response.SUCCESS

    # Checking input data
    data = request.get_json(force=True)

    conditions = [
        'title' not in data,
        'content' not in data,
        'price' not in data,
        'is_negotiable' not in data,
        'degree_course' not in data,
        'subject' not in data,
        'semester' not in data,
    ]
    if any(conditions):
        return response.BAD_REQUEST

    # Checking if degree_course exists
    degree_course = DegreeCourse.query.filter_by(degree_course=data['degree_course']).first()
    if degree_course is None:
        return response.CONFLICT

    # Checking if subject exists
    subject = Subject.query.filter_by(subject=data['subject'],
                                      degree_course_id=degree_course.id,
                                      semester=data['semester']).first()
    if subject is None:
        return response.CONFLICT

    # Updating announcement
    announcement.title = data['title']
    announcement.content = data['content']
    announcement.price = data['price']
    announcement.is_negotiable = data['is_negotiable']
    announcement.user_id = user_id
    announcement.subject_id = subject.id

    commit_database()

    return response.SUCCESS
