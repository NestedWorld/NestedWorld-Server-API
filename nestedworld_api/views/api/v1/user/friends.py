from flask import jsonify, request
from marshmallow import post_dump
from nestedworld_api.app import ma
from nestedworld_api.login import login_required, current_session
from . import user

user_friend = user.namespace('friends')


@user_friend.route('/')
class UserFriend(user_friend.Resource):

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        friend = ma.String()
        user = ma.String()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'friends' if many else 'friend'
            return {namespace: data}

    @login_required
    @user_friend.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import UserFriend

        friends = UserFriend.query.all()
        return friends

    @login_required
    @user_friend.accept(Schema())
    @user_friend.marshal_with(Schema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import UserFriend
        from nestedworld_api.db import User

        choosedFriend = User.query.filter(
            User.pseudo == data['friend']).first()
        if choosedFriend is None:
            auth.abort(400, message='Friend not found')

        friend = UserFriend()
        friend.user = current_session.user
        friend.friend = choosedFriend

        db.session.add(friend)
        db.session.commit()

        return friend
