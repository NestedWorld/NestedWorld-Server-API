import arrow
import sqlalchemy_utils as sau
from nestedworld_api.db import db


class MonsterAttack(db.Model):

    __tablename__ = 'monsterAttack'

    id = db.Column(db.Integer, primary_key=True, doc='MonsterAttack ID')

    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'))
    attack_id = db.Column(db.Integer, db.ForeignKey('attacks.id'))

    monster = db.relationship('Monster')
    attack = db.relationship('Attack')
