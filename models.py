from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Profile fields
    bio = db.Column(db.Text, nullable=True)
    github = db.Column(db.String(100), nullable=True)
    tech_stack = db.Column(db.String(100), nullable=True)
    profile_photo = db.Column(db.String(120), default='default.png', nullable=True)