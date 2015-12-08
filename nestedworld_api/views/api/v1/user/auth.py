from marshmallow import post_dump
from nestedworld_api.app import ma
from nestedworld_api.login import get_session, login_required
from . import user

auth = user.namespace('auth')

# Login

# Login > Simple (User/password + app token)


@auth.route('/login/simple')
class Login(auth.Resource):

    '''
        Simple login endpoint.
        Only use user/password pair and the application token.
    '''

    class UserSchema(ma.Schema):
        email = ma.Email()
        password = ma.String()
        app_token = ma.String()
        data = ma.Raw()

    class SessionSchema(ma.Schema):
        token = ma.String()

    @auth.accept(UserSchema(partial=True))
    @auth.marshal_with(SessionSchema())
    def post(self, data):
        '''
            Simple login with user/password pair and the application token.
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import User, Application, Session

        user = User.query.filter(
            User.email == data['email'], User.is_active == True).first()
        if user is None or user.password != data['password']:
            auth.abort(400, message='Cannot connect: Wrong email and/or password.')

        app = Application.query.filter(
            Application.token == data['app_token']).first()
        if app is None:
            auth.abort(400, message='Bad application token')

        session = Session(application=app, user=user, data=data.get('data'))
        db.session.add(session)
        db.session.commit()

        return session

# Register

@auth.route('/register')
class Register(auth.Resource):

    class Schema(ma.Schema):
        email = ma.Email()
        password = ma.String()
        pseudo = ma.String()

    @auth.accept(Schema())
    @auth.marshal_with(Schema())
    def post(self, data):
        '''
            Register a user.
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Application, User


        user = User.query.filter(User.email == data['email']).first()
        if user is not None:
            auth.abort(409, message='User already exists')

        user = User()
        user.email = data['email']
        user.password = data['password']
        user.pseudo = data['pseudo']

        db.session.add(user)
        db.session.commit()

        return user

# Lost password

@auth.route('/resetpassword')
class ResetPassword(auth.Resource):

    class Schema(ma.Schema):
        email = ma.Email()

    @auth.accept(Schema())
    def post(self, data):
        '''
            Request a password reset.
        '''

        from nestedworld_api.db import db
        from nestedworld_api.db import User, PasswordResetRequest
        from nestedworld_api.mail import TemplatedMessage

        user = User.query.filter(
            User.email == data['email'], User.is_active == True).first()
        if user is None:
            auth.abort(400, message='User not found')

        request = PasswordResetRequest(user=user)
        db.session.add(request)
        db.session.commit()

        message = TemplatedMessage('mail/password_reset.txt', token=request.token)
        message.add_recipient(user.email)
        message.send()

        return 'OK'

# Logout

@auth.route('/logout')
class Logout(auth.Resource):

    @login_required
    def post(self):
        import arrow
        from nestedworld_api.db import db

        session = get_session()
        if session is None:
            auth.abort(401)

        session.end = arrow.utcnow()

        db.session.commit()

        return 'OK'
