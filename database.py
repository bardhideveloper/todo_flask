from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    theme = db.Column(db.String(10), default="light")  # light or dark

    email = db.Column(db.String(120), unique=True, nullable=False)
    birthdate = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)

    tasks = db.relationship("Task", backref="user", lazy=True, cascade="all, delete-orphan")


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.String(20))
    priority = db.Column(db.String(10), default="Medium")
    order = db.Column(db.Integer, default=0)

    created_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
