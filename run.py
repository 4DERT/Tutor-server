from tutor import app
from tutor.database import create_db

if __name__ == '__main__':
    create_db()
    app.run(port=8080, debug=True, host="0.0.0.0")
