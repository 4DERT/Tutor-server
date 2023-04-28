from tutor import app, PORT, IS_DEBUG
from tutor.database import create_db

if __name__ == '__main__':
    with app.app_context():
        create_db()
        app.run(port=PORT, debug=IS_DEBUG, host="0.0.0.0")
