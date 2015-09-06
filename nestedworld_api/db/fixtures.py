from . import db
from .token import Application
from .user import User


def add(*objects):
    for o in objects:
        db.session.add(o)


def reset_db():
    # Reset users
    admin = User(
        email='kokakiwi@kokakiwi.net', password='kiwi3219', is_activated=True)

    add(admin)

    # Reset apps
    app = Application(name='Test app', token='test')

    add(app)
