import arrow
import sqlalchemy_utils as sau
from flask.ext.login import UserMixin
from . import db
from ..settings import PASSWORD_SCHEMES

PasswordType = sau.PasswordType(schemes=PASSWORD_SCHEMES)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, doc='User ID')

    email = db.Column(db.String(64), nullable=False, doc='User email')
    password = db.Column(PasswordType, nullable=False, doc='User password')

    registered_at = db.Column(
        sau.ArrowType, default=arrow.utcnow, doc='User registration date')

    is_active = db.Column(
        db.Boolean, nullable=False, default=True, doc='Is the user active?')
    is_activated = db.Column(
        db.Boolean, nullable=False, default=False, doc='Is the user activated?')
