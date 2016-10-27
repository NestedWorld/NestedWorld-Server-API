import unittest
from ... import TestCase


class LoginTestCase(TestCase):

    def test_valid_login(self):
        rv = self.login('kokakiwi@kokakiwi.net', 'kiwi3291', app_token='test')
        self.assertEqual(rv.status_code, 200)

    def test_bad_password(self):
        rv = self.login('kokakiwi@kokakiwi.net', 'toto')
        self.assertNotEqual(rv.status_code, 200)
        self.assertEqual(rv.json['message'], 'Cannot connect: Wrong email and/or password.')

    def test_bad_app_token(self):
        rv = self.login('kokakiwi@kokakiwi.net', 'kiwi3291', app_token='fake')
        self.assertNotEqual(rv.status_code, 200)
        self.assertEqual(rv.json['message'], 'Bad application token')

class RegisterTestCase(TestCase):

    def test_valid_register(self):
        from nestedworld_api.app import app, db
        from nestedworld_api.db import User

        with app.app_context():
            User.query.filter(User.email == 'test@bob.com').delete()
            db.session.commit()

        rv = self.tester.post('/users/auth/register', data={
            'email': 'test@bob.com',
            'password': 'bob',
            'pseudo': 'Spongebob',
        })
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json['email'], 'test@bob.com')


class LogoutTestCase(TestCase):

    def test_logout(self):
        rv = self.login('kokakiwi@kokakiwi.net', 'kiwi3291', app_token='test')
        token = rv.json['token']

        rv = self.logout(token)
        self.assertEqual(rv.status_code, 200)

    def test_invalid_session(self):
        rv = self.logout('not_valid')
        self.assertNotEqual(rv.status_code, 200)
