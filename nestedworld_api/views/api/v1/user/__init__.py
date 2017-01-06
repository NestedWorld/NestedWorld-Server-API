from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from nestedworld_api.login import login_required, current_session
from .. import api
from ..geo import PointField

users = api.namespace('users')

from . import auth
from . import monsters
from . import friends
from . import inventory
from . import stats


@users.route('/')
class Users(users.Resource):
    tags = ['users']

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        email = ma.Email()
        pseudo = ma.String()
        birth_date = ma.Date()
        city = ma.String()
        gender = ma.String(validate=[OneOf(['female', 'male', 'other'])])
        avatar = ma.Url()
        background = ma.Url()
        registered_at = ma.DateTime(dump_only=True)
        is_active = ma.Boolean(dump_only=True)
        level = ma.Integer()
        actual_localisation = PointField(attribute='point')
        is_connected = ma.Boolean()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'users' if many else 'user'
            return {namespace: data}

    @users.marshal_with(Schema(many=True))
    def get(self):
        '''
            Retrieve all users

            This request is used by a user for retrieve all users.
        '''

        from nestedworld_api.db import User as DbUser

        users = DbUser.query.all()

        return users


@users.route('/me')
class Me(users.Resource):

    class Schema(Users.Schema):
        pass

    @login_required
    @users.marshal_with(Schema())
    def get(self):
        '''
            Retrieve current user informations

            This request is used by a user for retrieve his own information.
        '''

        return current_session.user

    @login_required
    @users.accept(Schema())
    @users.marshal_with(Schema())
    def put(self, data):
        '''
            Update current user informations

            This request is used by a user for update his own information.
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import User as DbUser

        user = current_session.user

        if 'email' in data and DbUser.query.filter(User.email == data['email']).count() > 0:
            users.abort(400, message='An user with same email/pseudo already exists')
        if 'pseudo' in data and DbUser.query.filter(User.pseudo == data['pseudo']).count() > 0:
            users.abort(400, message='An user with same email/pseudo already exists')

        for (name, value) in data.items():
            setattr(user, name, value)

        db.session.commit()
        return user


@users.route('/<user_id>')
class User(users.Resource):
    tags = ['users']

    class Schema(Users.Schema):
        pass

    @users.marshal_with(Schema())
    def get(self, user_id):
        '''
            Retrieve user informations

            This request is used by a user for retrieve the information
            of a specific user (like a friend) or himself.
        '''
        from nestedworld_api.db import User as DbUser

        user = DbUser.query.get_or_404(user_id)
        return user

    @login_required
    @users.marshal_with(Schema())
    def put(self, data, user_id):
        '''
            Update user informations

            This request is used by a user for update the information
            of a specific user (like a friend) or himself.
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import User as DbUser

        user = DbUser.query.get_or_404(user_id)
        conflict = DbUser.query\
                         .filter(DbPortal.id != portal_id)\
                         .filter(DbPortal.pseudo == data['pseudo'])\
                         .first()

        if conflict is not None:
            users.abort(400, message='A user have already the same pseudonyme')

        for (name, value) in data.items():
            setattr(user, name, value)

        db.session.commit()

        return user
