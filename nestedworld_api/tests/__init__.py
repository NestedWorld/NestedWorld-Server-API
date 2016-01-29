import flask
import json
import unittest


# API tester classes
class JSONResponse(flask.Response):

    def get_json(self):
        return json.loads(self.get_data(as_text=True))

    @property
    def json(self):
        return self.get_json()


class APITester(object):

    base_url = '/v1'

    def __init__(self):
        from nestedworld_api.app import app

        app.testing = True
        app.response_class = JSONResponse
        self.app = app.test_client()

    # General request methods
    def _prepare_kwargs(self, data=None, headers=None):
        kwargs = {
            'data': None,
            'follow_redirects': True,
            'headers': {},
        }

        if data is not None:
            kwargs['data'] = json.dumps(data)
            kwargs['content_type'] = 'application/json'
        if headers is not None:
            kwargs['headers'].update(headers)

        return kwargs

    def get(self, path, headers=None):
        url = self.base_url + path
        kwargs = self._prepare_kwargs(headers=headers)

        return self.app.get(url, **kwargs)

    def post(self, path, data=None, headers=None):
        url = self.base_url + path
        kwargs = self._prepare_kwargs(data=data, headers=headers)

        return self.app.post(url, **kwargs)

    def put(self, path, data=None, headers=None):
        url = self.base_url + path
        kwargs = self._prepare_kwargs(data=data, headers=headers)

        return self.app.put(url, **kwargs)


# Base test case
class TestCase(unittest.TestCase):

    tester = APITester()

    # Auth helpers
    AUTH_HEADER_NAME = 'Authorization'
    AUTH_HEADER_VALUE = 'Bearer {0}'

    def login(self, email, password, app_token='test'):
        return self.tester.post('/users/auth/login/simple', data={
            'email': email,
            'password': password,
            'app_token': app_token,
        })

    def logout(self, token):
        return self.tester.post('/users/auth/logout', headers={
            self.AUTH_HEADER_NAME: self.AUTH_HEADER_VALUE.format(token)
        })
