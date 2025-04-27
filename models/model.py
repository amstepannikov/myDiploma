from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import constants as USER


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now,  onupdate=datetime.now)
    role = db.Column(db.SmallInteger, nullable=False, default=USER.USER)
    status = db.Column(db.SmallInteger, nullable=False, default=USER.NEW)

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    # Расширением предъявляются некоторые требования к классу User, а именно реализация следующих методов
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_status(self):
        return USER.STATUS[self.status]

    def get_role(self):
        return USER.ROLE[self.role]

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)


# from flask.ext.bcrypt import generate_password_hash, check_password_hash
#
# class User(db.Model):
#     ...
#     def check_password(self, password):
#         return check_password_hash(self.password, password)
#
#     @staticmethod
#     def hash_password(password):
#         return generate_password_hash(password)