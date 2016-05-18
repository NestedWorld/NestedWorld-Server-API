import intervals
import sqlalchemy_utils as sau
from . import Region
from . import Place
from .. import db
from ..monster import Monster
from ..utils import IDColumn

# FIXME: Hack to make SQLAlchemy-Utils Range type works
if not hasattr(intervals, 'canonicalize'):
    intervals.canonicalize = intervals.interval.canonicalize

class PlaceMonster(db.Model):

    __tablename__ = 'place_monsters'

    id = IDColumn()

    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'))

    place = db.relationship('Place', backref=db.backref('monsters'))
    monster = db.relationship('Monster')

class RegionMonster(db.Model):

    __tablename__ = 'region_monsters'

    id = IDColumn()

    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'))

    ratio = db.Column(db.Float, doc='Spawn rate')
    level = db.Column(sau.IntRangeType)

    region = db.relationship('Region', backref=db.backref('monsters'))
    monster = db.relationship('Monster')
