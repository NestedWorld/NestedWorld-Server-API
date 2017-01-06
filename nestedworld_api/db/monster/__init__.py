import arrow
import sqlalchemy_utils as sau
from nestedworld_api.db import db

from ..commons import elements
from .attacks import MonsterAttack

TYPES = ['water', 'fire', 'earth', 'electric', 'plant']


class Monster(db.Model):

    __tablename__ = 'monsters'

    id = db.Column(db.Integer, primary_key=True, doc='Monster ID')

    name = db.Column(db.String, doc='Monster name')

    hp = db.Column(db.Float, doc='Monster initial HP value')
    attack = db.Column(db.Float, doc='Monster initial attack value')
    defense = db.Column(db.Float, doc='Monster initial defense value')
    speed = db.Column(db.Float, doc='Monster initial speed value')
    type = db.Column(elements, doc='Monster type')
    base_sprite = db.Column(db.String, doc='Monster base sprite')
    enraged_sprite = db.Column(db.String(2000), nullable=True, doc='Monster enraged sprite')
