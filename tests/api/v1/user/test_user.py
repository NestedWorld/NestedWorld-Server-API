import unittest
from ... import TestCase


class UsersTestCase(TestCase):

    def test_infos(self):
        rv = self.login('kokakiwi@kokakiwi.net', 'kiwi3291')
        token = rv.json['token']

        rv = self.tester.get('/users/', headers={
            self.AUTH_HEADER_NAME: self.AUTH_HEADER_VALUE.format(token),
        })
        print(rv)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json['user']['email'], 'kokakiwi@kokakiwi.net')
