from . import db
from .token import Application
from .user import User
from datetime import date

def add(*objects):
    for o in objects:
        db.session.add(o)


def reset_db():
    # Reset users
    admin = User(
        email='kokakiwi@kokakiwi.net', password='kiwi3219', is_activated=True,
        pseudo='kokakiwi', city='Seoul', birth_date=date(1992, 8, 10), gender='male')
    florian = User(
        email='florian.faisan@epitech.eu', password='florian', is_activated=True,
        pseudo='kassisdion', city='Seoul', birth_date=date(1993, 9, 12), gender='male')

    add(admin, florian)

    # Reset apps
    app = Application(name='Test app', token='test')

    add(app)
