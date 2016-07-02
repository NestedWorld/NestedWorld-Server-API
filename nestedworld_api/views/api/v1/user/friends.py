from flask import jsonify, request
from marshmallow import post_dump
from nestedworld_api.app import ma
from nestedworld_api.login import login_required, current_session
from . import user

user_friend = user.namespace('friends')


@user_friend.route('/')
class UserFriend(user_friend.Resource):
    tags = ['users']

    class FriendResult(ma.Schema):

        #TODO : Maybe use the User.Schema ?
        class User(ma.Schema):
            pseudo = ma.String()
            birth_date = ma.Date()
            city = ma.String()
            gender = ma.String()
            avatar = ma.Url()
            background = ma.Url()
            registered_at = ma.DateTime(dump_only=True)
            level = ma.Integer()
            is_connected = ma.Boolean()

        user = ma.Nested(User, attribute='friend')

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'friends' if many else 'friend'
            return {namespace: data}

    class FriendRequest(ma.Schema):

        pseudo = ma.String()

    @login_required
    @user_friend.marshal_with(FriendResult(many=True))
    def get(self):
        from nestedworld_api.db import UserFriend

        friends = UserFriend.query\
                            .filter((UserFriend.user_id == current_session.user.id) |
                                    (UserFriend.friend_id == current_session.user.id))\
                            .all()
        return friends

    @login_required
    @user_friend.accept(FriendRequest())
    @user_friend.marshal_with(FriendResult())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import User, UserFriend

        friend = User.query.filter(
            User.pseudo == data['pseudo']).first()
        if friend is None:
            user.abort(400, message='Friend not found')

        user_friend = UserFriend(user=current_session.user, friend=friend)
        db.session.add(user_friend)
        db.session.commit()

        return user_friend
