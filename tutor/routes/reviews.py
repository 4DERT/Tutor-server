from flask import request

from tutor import app, session, response
from tutor.database import get_user_by_username, insert_into_database
from tutor.models import Review


@app.route("/add_review", methods=["POST"])
def add_review():
    data = request.get_json(force=True)

    # Checking input data
    if 'reviewee' not in data or 'rate' not in data:
        return response.BAD_REQUEST

    reviewee_username = data["reviewee"]
    rate = data["rate"]
    review = data["review"] if "review" in data else None  # review is optional

    if int(rate) < 1 or int(rate) > 5:
        return response.BAD_REQUEST

    # Checking if user is logged
    if 'user_id' not in session:
        return response.UNAUTHORIZED

    user_id = session['user_id']

    # Checking if user exists
    reviewee = get_user_by_username(reviewee_username)
    if reviewee is None:
        return response.CONFLICT

    # Check if user already add review to given person
    for revs in reviewee.reviews_received:
        if revs.reviewer_id == user_id:
            return response.CONFLICT

    insert_into_database(
        Review(
            rate=rate,
            review=review,
            reviewer_id=user_id,
            reviewee_id=reviewee.id)
    )

    return response.SUCCESS
