import arrow
import sqlalchemy_utils as sau
from . import db


class Attack(db.Model):

    __tablename__ = 'attacks'

    id = db.Column(db.Integer, primary_key=True, doc='Attack ID')

    name = db.Column(db.String, doc='Attack name')
    type = db.Column(db.Enum('attack', 'attacksp', 'defense', 'defensesp',
                             name='attack_types'), doc='Attack type')
    sprite = db.Column(db.String(2000), nullable=True, doc='Attack spriter')
