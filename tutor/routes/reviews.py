from flask import request

from tutor import app, session, response
from tutor.database import get_user_by_username, insert_into_database, \
    delete_from_database, commit_database, get_review
from tutor.models import Review


@app.route("/user/<username>/review", methods=["POST", "PUT", "DELETE"])
def add_review(username: str):
    # Checking if user is logged
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']

    reviewee = get_user_by_username(username)

    # Find review
    rev = get_review(reviewee, user_id)

    if request.method == 'DELETE':
        if rev is None:
            return response.CONFLICT

        delete_from_database(rev)
        return response.SUCCESS

    # get json data
    data = request.get_json(force=True)

    # Checking input data
    if 'rate' not in data:
        return response.BAD_REQUEST

    rate = data["rate"]
    review = data["review"] if "review" in data else None  # review is optional

    if int(rate) < 1 or int(rate) > 5:
        return response.BAD_REQUEST

    if request.method == 'PUT':
        if rev is None:
            return response.CONFLICT

        rev.rate = rate
        rev.review = review
        commit_database()

        return response.SUCCESS

    if request.method == 'POST':
        if rev is not None:
            return response.CONFLICT

        insert_into_database(
            Review(
                rate=rate,
                review=review,
                reviewer_id=user_id,
                reviewee_id=reviewee.id)
        )

        return response.SUCCESS

    return response.BAD_REQUEST
