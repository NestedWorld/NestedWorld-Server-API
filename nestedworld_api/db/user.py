import arrow
import sqlalchemy_utils as sau
from . import db
from ..settings import PASSWORD_SCHEMES

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
        sau.ArrowType, default=arrow.utcnow, doc='User registration date')

    is_active = db.Column(
        db.Boolean, nullable=False, default=True, doc='Is the user active?')

    pseudo = db.Column(db.String(32), nullable=False, unique=True,
                       doc='User pseudo')
    city = db.Column(db.String(255), nullable=True, doc='User city')
    birth_date = db.Column(sau.ArrowType, nullable=True, doc='User Birth Date')
    gender = db.Column(
        db.Enum('female', 'male', 'other', name='gender_types'),
        nullable=True, doc='User gender')


class PasswordResetRequest(db.Model):

    __tablename__ = 'password_reset_requests'

    id = db.Column(db.Integer, primary_key=True, doc='Request ID')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(
        db.String(32), nullable=False, default=random_token,
        doc='Request token', index=True)

    user = db.relationship(User)
