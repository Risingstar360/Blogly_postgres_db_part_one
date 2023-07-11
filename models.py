from flask_sqlalchemy import SQLAlchemy

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
    image_url = db.Column(db.Text, nullable=False, default="holding_image")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


def connect_db(app):

    db.app = app
    db.init_app(app)


# """SQLAlchemy models for blogly."""

# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


# class User(db.Model):
#     """Site user."""

#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.Text, nullable=False)
#     last_name = db.Column(db.Text, nullable=False)
#     image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

#     @property
#     def full_name(self):
#         """Return full name of user."""

#         return f"{self.first_name} {self.last_name}"


# def connect_db(app):
#     """Connect this database to provided Flask app.

#     You should call this in your Flask app.
#     """

#     db.app = app
#     db.init_app(app)
