from flask.ext.restplus import Resource
from nestedworld_api.login import login_required, current_session
from .. import api

user = api.namespace('users', description='User operations')


from . import auth


@user.route('/')
class User(Resource):

    __apidoc__ = {
        'params': auth.AUTH_REQUIRED_PARAMS,
    }

    @login_required
    def get(self):
        import json

        data = {}

        data['email'] = current_session.user.email
        data['registered_at'] = str(current_session.user.registered_at)
        data['is_active'] = current_session.user.is_active
        data['pseudo'] = current_session.user.pseudo
        data['birth_date'] = str(current_session.user.birth_date)
        data['city'] = current_session.user.city
        data['gender'] = current_session.user.gender
        json_data = json.dumps(data)
        return json_data
