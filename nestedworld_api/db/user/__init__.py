import arrow
import sqlalchemy_utils as sau
from geoalchemy2 import Geography
from nestedworld_api.db import db
from nestedworld_api.settings import PASSWORD_SCHEMES


from .monsters import UserMonster
from .friends import UserFriend
from .inventory import Inventory


PasswordType = sau.PasswordType(schemes=PASSWORD_SCHEMES)


def random_token():
    import uuid

    return uuid.uuid4().hex


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, doc='User ID')

    email = db.Column(db.String(64), nullable=False, doc='User email')
    password = db.Column(PasswordType, nullable=False, doc='User password')

    registered_at = db.Column(
        sau.ArrowType(timezone=True), default=arrow.utcnow, doc='User registration date')

    is_active = db.Column(
        db.Boolean, nullable=False, default=True, doc='Is the user active?')

    is_connected = db.Column(
        db.Boolean, nullable=False, default=False, doc="Is the user connected?")

    pseudo = db.Column(db.String(32), nullable=False, unique=True,
                       doc='User pseudo')
    city = db.Column(db.String(255), nullable=True, doc='User city')
    birth_date = db.Column(db.Date, nullable=True, doc='User Birth Date')
    gender = db.Column(
        db.Enum('female', 'male', 'other', name='gender_types'),
        nullable=True, doc='User gender')
    avatar = db.Column(db.String(2000), nullable=True, doc='User Avatar')
    background = db.Column(db.String(2000), nullable=True,
                           doc='User Background')
    level = db.Column(db.Integer, doc="User level", default=0)

    actual_localisation = db.Column(Geography('POINT'), doc='User Actual position')

class PasswordResetRequest(db.Model):

    __tablename__ = 'password_reset_requests'

    id = db.Column(db.Integer, primary_key=True, doc='Request ID')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(
        db.String(32), nullable=False, default=random_token,
        doc='Request token', index=True)

    user = db.relationship(User)
