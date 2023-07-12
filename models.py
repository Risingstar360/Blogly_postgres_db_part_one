from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

holding_image = "https://www.freeiconspng.com/uploads/person-icon-145444--bryan-le-photography-7.png"


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=holding_image)
    posts = db.relationship('Post', backref='user',
                            cascade='all, delete-orphan')


class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.user.first_name} {self.user.last_name}"


def connect_db(app):
    db.app = app
    db.init_app(app)
