from flask.ext.restplus import Resource
from flask.ext.restplus import fields
from nestedworld_api.db import db
from nestedworld_api.login import get_session, login_required
from . import user

auth = user.namespace('auth', description='User auth operations')

AUTH_REQUIRED_PARAMS = {
    'Authorization': {
        'description': 'Session token. Format: Bearer [TOKEN]',
        'in': 'header',
    }
}

# Login

# Login > Simple (User/password + app token)


@auth.route('/login/simple')
class Login(Resource):

    '''
        Simple login endpoint.
        Only use user/password pair and the application token.
    '''

    parser = auth.parser()
    parser.add_argument(
        'email', type=str, required=True, help='User email', location='form')
    parser.add_argument(
        'password', type=str, required=True, help='User password', location='form')
    parser.add_argument(
        'app_token', type=str, required=True, help='Application token', location='form')
    parser.add_argument(
        'data', required=False, help='Additional session data', location='form')

    result = auth.model('LoginResult', {
        'token': fields.String(required=True, description='Session token'),
    })

    @auth.doc(parser=parser)
    @auth.marshal_with(result)
    def post(self):
        '''
            Simple login with user/password pair and the application token.
        '''
        import json
        from nestedworld_api.db import db
        from nestedworld_api.db import User, Application, Session

        args = Login.parser.parse_args()

        user = User.query.filter(
            User.email == args.email, User.is_active == True).first()
        if user is None or user.password != args.password:
            auth.abort(400, 'User not found')

        app = Application.query.filter(
            Application.token == args.app_token).first()
        if app is None:
            auth.abort(400, 'Bad application token')

        data = None
        try:
            data = json.loads(args.data)
        except:
            pass

        session = Session(application=app, user=user, data=data)
        db.session.add(session)
        db.session.commit()

        return {'token': session.token}

# Register

@auth.route('/register')
class Register(Resource):

    parser = auth.parser()
    parser.add_argument(
        'email', type=str, required=True, help='User email', location='form')
    parser.add_argument(
        'password', type=str, required=True, help='User password', location='form')
    parser.add_argument(
        'pseudo', type=str, required=True, help='User pseudonyme', location='form')

    result = auth.model('User', {
        'email': fields.String(required=True, description='User email'),
    })

    @auth.doc(parser=parser)
    @auth.marshal_with(result, envelope='user')
    def post(self):
        '''
            Register a user.
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Application, User

        args = Register.parser.parse_args()

        user = User.query.filter(User.email == args.email).first()
        if user is not None:
            auth.abort(409, 'User already exists')

        user = User()
        user.email = args.email
        user.password = args.password
        user.pseudo = args.pseudo

        db.session.add(user)
        db.session.commit()

        return user

# Lost password

@auth.route('/resetpassword')
class ResetPassword(Resource):

    parser = auth.parser()
    parser.add_argument(
        'email', type=str, required=True, help='User email', location='form')

    @auth.doc(parser=parser)
    def post(self):
        '''
            Request a password reset.
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import User, PasswordResetRequest
        from nestedworld_api.mail import TemplatedMessage

        args = ResetPassword.parser.parse_args()

        user = User.query.filter(
            User.email == args.email, User.is_active == True).first()
        if user is None:
            auth.abort(400, 'User not found')

        request = PasswordResetRequest(user=user)
        db.session.add(request)
        db.session.commit()

        message = TemplatedMessage('mail/password_reset.txt', token=request.token)
        message.add_recipient(user.email)
        message.send()

        return 'OK'

# Logout

@auth.route('/logout')
class Logout(Resource):

    __apidoc__ = {
        'params': AUTH_REQUIRED_PARAMS,
    }

    @login_required
    def get(self):
        import arrow

        session = get_session()
        session.end = arrow.utcnow()

        db.session.add(session)
        db.session.commit()
