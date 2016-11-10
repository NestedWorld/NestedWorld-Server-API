import arrow
import sqlalchemy_utils as sau
from geoalchemy2 import Geometry, Geography
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.sql.expression import cast
from .. import db
from ..utils import IDColumn


class Portal(db.Model):

    __tablename__ = 'portals'

    id = IDColumn(doc='Portal ID')

    name = db.Column(db.String, doc='Portal name')
    description = db.Column(db.Text, doc='Portal description')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    added_at = db.Column(
        sau.ArrowType, default=arrow.utcnow, doc='Portal addition date')

    point = db.Column(Geography('POINT'), doc='Portal geography point')

    author = db.relationship('User')


class Region(db.Model):

    __tablename__ = 'regions'

    id = IDColumn(doc='Region ID')

    name = db.Column(db.String, doc='Region name')

    zone = db.Column(Geography('MULTIPOLYGON'), doc='Region geography polygon')

    @hybrid_property
    def portals(self):
        return Portal.query\
                    .filter(func.ST_intersects(self.zone, Portal.point))

from .monsters import RegionMonster
from .monsters import PortalMonster
