import arrow
import sqlalchemy_utils as sau
from itsdangerous import JSONWebSignatureSerializer as Serializer
from . import db
from ..settings import SECRET_KEY


serializer = Serializer(SECRET_KEY)


def random_token():
    import uuid

    return uuid.uuid4().hex


class Application(db.Model):

    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True, doc='Application ID')

    name = db.Column(db.String, nullable=False, doc='Application name')
    token = db.Column(
        db.String(32), nullable=False, default=random_token, doc='Application token', index=True)


class Session(db.Model):

    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True, doc='Application ID')

    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    start = db.Column(sau.ArrowType, nullable=False, default=arrow.utcnow)
    end = db.Column(sau.ArrowType, nullable=True)

    data = db.Column(sau.JSONType, nullable=True)

    application = db.relationship('Application')
    user = db.relationship('User')

    @property
    def token(self):
        data = {
            'session_id': self.id,
        }

        return serializer.dumps(data).decode('utf-8')

    @staticmethod
    def decode_token(token, allow_expired=False):
        import arrow

        try:
            data = serializer.loads(token.encode('utf-8'))
        except:
            return None

        session = Session.query.filter(
            Session.id == data['session_id']).first()
        if not allow_expired and session is not None and session.end is not None and arrow.utcnow() > session.end:
            return None

        return session
