from tutor import app, PORT, IS_DEBUG
from tutor.database import create_db


def wsgi():
    with app.app_context():
        create_db()

    return app


if __name__ == '__main__':
    with app.app_context():
        create_db()
        app.run(port=PORT, debug=IS_DEBUG, host="0.0.0.0")
