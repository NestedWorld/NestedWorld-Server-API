from flask.ext.restplus import Resource
from flask.ext.restplus import fields
from nestedworld_api.db import db
from nestedworld_api.login import get_session, login_required
from . import user

auth = user.namespace('auth')

# Login

# Login > Simple (User/password + app token)


@auth.route('/login/simple')
class Login(Resource):

    '''
        Simple login endpoint.
        Only use user/password pair and the application token.
    '''

    def post(self):
        '''
            Simple login with user/password pair and the application token.
        '''
        auth.abort(501)

# Register

@auth.route('/register')
class Register(Resource):

    def post(self):
        '''
            Register a user.
        '''
        auth.abort(501)

# Lost password

@auth.route('/resetpassword')
class ResetPassword(Resource):

    def post(self):
        '''
            Request a password reset.
        '''
        auth.abort(501)

# Logout

@auth.route('/logout')
class Logout(Resource):

    @login_required
    def get(self):
        import arrow

        session = get_session()
        session.end = arrow.utcnow()

        db.session.add(session)
        db.session.commit()
