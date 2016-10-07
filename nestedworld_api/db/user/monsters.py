import arrow
import sqlalchemy_utils as sau
from nestedworld_api.db import db


class UserMonster(db.Model):

    __tablename__ = 'user_monsters'

    id = db.Column(db.Integer, primary_key=True, doc='UserMonster ID')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'))

    surname = db.Column(db.String, doc="Monster surname")
    experience = db.Column(db.Integer, doc="Monster experience")
    level = db.Column(db.Integer, doc="Monster level")

    monster = db.relationship('Monster', cascade="all", backref=db.backref('user_monsters'))
    user = db.relationship('User', cascade="all", backref=db.backref('user_monsters'))
