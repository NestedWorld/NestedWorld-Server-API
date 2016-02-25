from flask.ext import restful
from . import helpers


def _make_shortcut(f):
    def wrapper(self, *args, **kwarg):
        return f(*args, **kwarg)
    return wrapper


class Shortcuts(object):

    Resource = restful.Resource

    accept = _make_shortcut(helpers.accept)
    marshal_with = _make_shortcut(helpers.marshal_with)

    abort = _make_shortcut(restful.abort)
