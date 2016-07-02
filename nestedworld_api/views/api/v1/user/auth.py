from flask import jsonify
from marshmallow import post_dump
from nestedworld_api.app import ma
from nestedworld_api.login import get_session, login_required
from . import user

auth = user.namespace('auth')

# Login

# Login > Simple (User/password + app token)


@auth.route('/login/simple')
class Login(auth.Resource):
    tags = ['users.auth']

    class UserSchema(ma.Schema):
        email = ma.Email(required=True)
        password = ma.String(required=True)
        app_token = ma.String(required=True)
        data = ma.Raw()

    class SessionSchema(ma.Schema):
        token = ma.String()

    @auth.accept(UserSchema())
    @auth.marshal_with(SessionSchema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import User, Application, Session

        user = User.query.filter(
            User.email == data['email'], User.is_active).first()
        if user is None or user.password != data['password']:
            auth.abort(400, message='Cannot connect: Wrong email and/or password.')

        app = Application.query.filter(
            Application.token == data['app_token']).first()
        if app is None:
            auth.abort(400, message='Bad application token')

        setattr(user, "is_connected", True)
        session = Session(application=app, user=user, data=data.get('data'))
        db.session.add(session)
        db.session.commit()

        return session


# Register
@auth.route('/register')
class Register(auth.Resource):
    tags = ['users.auth']

    class Schema(ma.Schema):
        email = ma.Email(required=True)
        password = ma.String(required=True)
        pseudo = ma.String(required=True)

    @auth.accept(Schema())
    @auth.marshal_with(Schema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import Application, User

        user = User.query.filter(User.email == data['email'] or User.pseudo == data['pseudo']).first()
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
    tags = ['users.auth']

    class Schema(ma.Schema):
        email = ma.Email(required=True)

    @auth.accept(Schema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import User, PasswordResetRequest
        from nestedworld_api.mail import TemplatedMessage

        user = User.query.filter(
            User.email == data['email'], User.is_active).first()
        if user is None:
            auth.abort(400, message='User not found')

        request = PasswordResetRequest(user=user)
        db.session.add(request)
        db.session.commit()

        message = TemplatedMessage('mail/password_reset.txt', token=request.token)
        message.add_recipient(user.email)
        message.send()

        return jsonify(message='Password reset request sent')


# Logout
@auth.route('/logout')
class Logout(auth.Resource):
    tags = ['users.auth']

    @login_required
    def post(self):
        import arrow
        from nestedworld_api.db import db

        session = get_session()
        if session is None:
            auth.abort(401)

        session.end = arrow.utcnow()
        setattr(user, "is_connected", False)

        db.session.commit()

        return jsonify(message='Successfully logged out')
