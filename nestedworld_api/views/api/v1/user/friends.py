from nestedworld_api.app import ma
from marshmallow import post_dump
from nestedworld_api.login import login_required, current_session
from . import users

user_friends = users.namespace('friends')


@user_friends.route('/')
class UserFriends(user_friends.Resource):
    tags = ['users']

    class FriendResult(ma.Schema):

        # TODO : Maybe use the User.Schema ?
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

        id = ma.Integer(dump_only=True)
        user = ma.Nested(User, attribute='friend')

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'friends' if many else 'friend'
            return {namespace: data}

    class FriendRequest(ma.Schema):

        pseudo = ma.String()

    @login_required
    @user_friends.marshal_with(FriendResult(many=True))
    def get(self):
        '''
            Retrieve current user's friends list.

            This request is used by a user for retrieve his own friends list.
        '''
        from nestedworld_api.db import UserFriend as DbUserFriend

        friends = DbUserFriend.query\
                              .filter(DbUserFriend.user_id == current_session.user.id)\
                              .all()
        return friends

    @login_required
    @user_friends.accept(FriendRequest())
    @user_friends.marshal_with(FriendResult())
    def post(self, data):
        '''
            Add an user in to current user's friends list

            This request is used by a user for create a link between him
            and another existing user as friend.
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import User as DbUser
        from nestedworld_api.db import UserFriend as DbUserFriend

        friend = DbUser.query.filter(
            DbUser.pseudo == data['pseudo']).first()
        if friend is None:
            user_friends.abort(400, message='Friend not found')

        friends_count = DbUserFriend.query\
                                    .filter((DbUserFriend.user_id == current_session.user.id) &
                                            (DbUserFriend.friend_id == friend.id))\
                                    .count()
        if friends_count > 0:
            user_friend.abort(400, message='Friend already added')

        result = DbUserFriend(user=current_session.user, friend=friend)
        db.session.add(result)
        db.session.commit()

        return result


@user_friends.route('/<friend_id>')
class UserFriend(user_friends.Resource):

    @login_required
    @user_friends.marshal_with(UserFriends.FriendResult())
    def get(self, friend_id):
        from nestedworld_api.db import UserFriend as DbUserFriend

        friend = DbUserFriend.query.filter(DbUserFriend.id == friend_id).first()
        return friend

    @login_required
    def delete(self, friend_id):
        '''
            delete an user in to current user's friends list

            This request is used by a user for deleting a link between him
            and another existing user as friend.
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import UserFriend as DbUserFriend

        DbUserFriend.query.filter(DbUserFriend.id == friend_id).delete()
        db.session.commit()
