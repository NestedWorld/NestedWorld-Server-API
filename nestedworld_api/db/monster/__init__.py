import arrow
import sqlalchemy_utils as sau
from nestedworld_api.db import db

from .attacks import MonsterAttack

class Monster(db.Model):

    __tablename__ = 'monsters'

    id = db.Column(db.Integer, primary_key=True, doc='Monster ID')

    name = db.Column(db.String, doc='Monster name')

    hp = db.Column(db.Float, doc='Monster initial HP value')
    attack = db.Column(db.Float, doc='Monster initial attack value')
    defense = db.Column(db.Float, doc='Monster initial defense value')
    type = db.Column(db.Enum('water', 'fire', 'earth', 'electric', 'plant',
                             name='monster_types'), doc='Monster type')
