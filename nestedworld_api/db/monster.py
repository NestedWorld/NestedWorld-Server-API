import arrow
import sqlalchemy_utils as sau
from . import db


class Monster(db.Model):

    __tablename__ = 'monsters'

    id = db.Column(db.Integer, primary_key=True, doc='Monster ID')

    name = db.Column(db.String, doc='Monster name')

    hp = db.Column(db.Float, doc='Monster initial HP value')
    attack = db.Column(db.Float, doc='Monster initial attack value')
    defense = db.Column(db.Float, doc='Monster initial defense value')
