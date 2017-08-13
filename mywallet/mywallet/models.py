"""Database models by SQLAlchemy ORM."""

import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model"""

    __tablename__ = 'user'

    singular = 'User'
    plural = 'Users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False)

    username = db.Column(db.String(255), unique=True)
    pw_hash = db.Column(db.Text, nullable=False)

    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now)

    trackings = db.relationship("UserTracking", back_populates="user")


class Category(db.Model):
    """Category model"""

    singular = 'Category'
    plural = 'Categories'

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now)


class Tag(db.Model):
    """Tag model"""

    singular = 'Tag'
    plural = 'Tags'

    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now)


class UserTracking(db.Model):
    """UserTracking model

    to track the user browsing
    """

    singular = 'User Tracking'
    plural = 'User Trackings'

    __tablename__ = 'usertracking'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ip = db.Column(db.String(255), nullable=False)
    url = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now)

    user = db.relationship("User", back_populates="trackings")
