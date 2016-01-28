from nestedworld_api.app import app

app.testing = True
test_app = app.test_client()


def test_working():
    pass
