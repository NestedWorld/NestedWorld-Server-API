import flask_restful as restful
from flask import request
from functools import wraps


def accept(schema, force=False):
    def wrapper(f):
        f.__accept__ = {
            'schema': schema,
            'force': force,
        }

        @wraps(f)
        def wrapped(*args, **kwargs):
            data = request.get_json(force=force)
            result = schema.load(data)

            if result.errors:
                restful.abort(412, message='Invalid input data', errors=result.errors)

            if result.data is None:
                restful.abort(400, message='Invalid input data')

            return f(*args, data=result.data, **kwargs)
        return wrapped
    return wrapper


def marshal_with(schema):
    def convert(data):
        data = schema.dump(data).data
        return data

    def wrapper(f):
        f.__marshal_with__ = {
            'schema': schema,
        }

        @wraps(f)
        def wrapped(*args, **kwargs):
            result = f(*args, **kwargs)

            if isinstance(result, tuple):
                (code, data) = result
                data = convert(data)

                result = (code, data)
            else:
                data = convert(result)

                result = data

            return result
        return wrapped
    return wrapper
