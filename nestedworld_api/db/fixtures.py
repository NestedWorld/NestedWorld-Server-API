from nestedworld_api.db import db
from nestedworld_api.db.token import Application
from nestedworld_api.db.user import User
from datetime import date
import arrow


def add(*objects):
    for o in objects:
        db.session.add(o)


def reset_db():
    # Reset users
    admin = User(
        email='kokakiwi@kokakiwi.net', pseudo='kokakiwi', city='Seoul',
        birth_date=arrow.get('1992-08-10'), gender='male')
    admin.password = 'kiwi3291'
    florian = User(
        email='florian.faisan@epitech.eu', pseudo='kassisdion', city='Seoul',
        birth_date=arrow.get('1993-09-12'), gender='male')
    florian.password = 'florian'

    alice = User(
        email='alice@bob.com', pseudo='alice', city='CCrypto',
        birth_date=arrow.get('2010-10-10'), gender='female')
    alice.password = 'bob'

    add(admin, florian, alice)

    # Reset apps
    app = Application(name='Test app', token='test')

    add(app)
