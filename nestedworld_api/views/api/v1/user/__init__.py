from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from nestedworld_api.login import login_required, current_session
from .. import api
from ..geo import PointField

user = api.namespace('users')

from . import auth
from . import monsters
from . import friends
from . import inventory


@user.route('/')
class User(user.Resource):
    tags = ['users']

    class Schema(ma.Schema):
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

    @login_required
    @user.marshal_with(Schema())
    def get(self):
        user = current_session.user

        return user

    @login_required
    @user.accept(Schema())
    @user.marshal_with(Schema())
    def put(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import User

        user = current_session.user

        if 'email' in data and User.query.filter(User.email == data['email']).count() > 0:
            user.abort(400, 'An user with same email/pseudo already exists')
        if 'pseudo' in data and User.query.filter(User.pseudo == data['pseudo']).count() > 0:
            user.abort(400, 'An user with same email/pseudo already exists')

        for (name, value) in data.items():
            setattr(user, name, value)

        db.session.commit()
        return user


@user.route('/<user_id>')
class UserId(user.Resource):
    tags = ['users']

    class Schema(User.Schema):
        pass

    @user.marshal_with(Schema())
    def get(self, user_id):
        from nestedworld_api.db import User as DbUser

        user = DbUser.query.get_or_404(user_id)
        return user

    @user.marshal_with(Schema())
    def put(self, data, user_id):
        from nestedworld_api.db import db
        from nestedworld_api.db import User as DbUser

        user = DbUser.query.get_or_404(user_id)
        conflict = DbUser.query\
                         .filter(DbPlace.id != place_id)\
                         .filter(DbPlace.pseudo == data['pseudo'])\
                         .first()

        if conflict is not None:
            places.abort(400, 'A user have already the same pseudonyme')

        for (name, value) in data.items():
            setattr(user, name, value)

        db.session.commit()

        return user
