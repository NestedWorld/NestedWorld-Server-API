from flask.ext.restplus import Resource
from nestedworld_api.login import login_required, current_session
from .. import api

user = api.namespace('user', description='User operations')


from . import auth


@user.route('/')
class User(Resource):

    __apidoc__ = {
        'params': auth.AUTH_REQUIRED_PARAMS,
    }

    @login_required
    def get(self):
        '''
            Get a hello message with some user informations.
        '''
        s = 'Hello %s, you are connected with "%s"' % (
            current_session.user.email, current_session.application.name)
        return s
