import arrow
import sqlalchemy_utils as sau
from nestedworld_api.db import db


class UserFriend(db.Model):

    __tablename__ = 'user_friends'

    id = db.Column(db.Integer, primary_key=True, doc='UserFriend ID')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    friend = db.relationship('User', foreign_keys='UserFriend.user_id')
    user = db.relationship('User', foreign_keys='UserFriend.user_id')
