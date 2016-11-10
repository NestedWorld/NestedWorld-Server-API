import intervals
import sqlalchemy_utils as sau
from . import Region
from . import Portal
from .. import db
from ..monster import Monster
from ..utils import IDColumn

# FIXME: Hack to make SQLAlchemy-Utils Range type works
if not hasattr(intervals, 'canonicalize'):
    intervals.canonicalize = intervals.interval.canonicalize

class PortalMonster(db.Model):

    __tablename__ = 'portal_monsters'

    id = IDColumn()

    portal_id = db.Column(db.Integer, db.ForeignKey('portals.id'))
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'))

    portal = db.relationship('Portal', cascade="all, delete", backref=db.backref('portal_monsters'))
    monster = db.relationship('Monster', cascade="all, delete", backref=db.backref('portal_monsters'))

class RegionMonster(db.Model):

    __tablename__ = 'region_monsters'

    id = IDColumn()

    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'))

    ratio = db.Column(db.Float, doc='Spawn rate')
    level = db.Column(sau.IntRangeType)

    region = db.relationship('Region', cascade="all, delete", backref=db.backref('region_monsters'))
    monster = db.relationship('Monster', cascade="all, delete", backref=db.backref('region_monsters'))
