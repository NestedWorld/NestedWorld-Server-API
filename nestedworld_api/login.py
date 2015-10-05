from flask import abort, request
from functools import wraps
from werkzeug.local import LocalProxy

__all__ = ['current_session', 'get_session', 'login_required']

current_session = LocalProxy(lambda: get_session())


def get_session(**kwargs):
    from .db import Session

    header = request.headers.get('Authorization')
    if header is None:
        return None

    token = header.replace('Bearer ', '', 1)
    session = Session.decode_token(token, **kwargs)

    return session


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        session = get_session(allow_expired=True)
        if session is None:
            abort(401)

        return f(*args, **kwargs)

    return wrapper
