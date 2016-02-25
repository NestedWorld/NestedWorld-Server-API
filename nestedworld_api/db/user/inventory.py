import arrow
import sqlalchemy_utils as sau
from nestedworld_api.db import db


class Inventory(db.Model):

    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True, doc='Inventory ID')

    object_id = db.Column(db.Integer, db.ForeignKey('objects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    object = db.relationship('Object')
    user = db.relationship('User')
