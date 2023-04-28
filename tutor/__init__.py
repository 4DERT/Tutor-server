from datetime import datetime
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from os import getenv

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY", "FIND_BETTER_KEY")
ADMINS = getenv("ADMINS", "").split(',')
PORT = getenv("PORT", "8080")
IS_DEBUG = getenv("IS_DEBUG", "False").lower() in ('true', '1')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from .routes import announcements, session, subjects, degree_courses, users, reviews
