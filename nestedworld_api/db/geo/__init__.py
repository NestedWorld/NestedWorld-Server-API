import arrow
import sqlalchemy_utils as sau
from geoalchemy2 import Geometry, Geography
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.sql.expression import cast
from .. import db
from ..utils import IDColumn


class Place(db.Model):

    __tablename__ = 'places'

    id = IDColumn(doc='Place ID')

    name = db.Column(db.String, doc='Place name')
    description = db.Column(db.Text, doc='Place description')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    added_at = db.Column(
        sau.ArrowType, default=arrow.utcnow, doc='Place addition date')

    point = db.Column(Geography('POINT'), doc='Place geography point')

    author = db.relationship('User')


class Region(db.Model):

    __tablename__ = 'regions'

    id = IDColumn(doc='Region ID')

    name = db.Column(db.String, doc='Region name')

    zone = db.Column(Geography('MULTIPOLYGON'), doc='Region geography polygon')

    @hybrid_property
    def places(self):
        return Place.query\
                    .filter(func.ST_intersects(self.zone, Place.point))

from .monsters import RegionMonster
