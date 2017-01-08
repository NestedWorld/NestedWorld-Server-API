import arrow
import sqlalchemy_utils as sau
from geoalchemy2 import Geometry, Geography
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.sql.expression import cast
from ..commons import elements
from .. import db
from ..utils import IDColumn


class Portal(db.Model):

    __tablename__ = 'portals'

    id = IDColumn(doc='Portal ID')

    name = db.Column(db.String, doc='Portal name')
    point = db.Column(Geography('POINT'), doc='Portal geography point')
    created = db.Column(sau.ArrowType(timezone=True), default=arrow.utcnow, doc='Portal creation date')
    captured = db.Column(sau.ArrowType(timezone=True), doc='Date of capture')
    captured_by = db.Column(db.Integer, doc="Id of the User that captured the portal")
    monster_on = db.Column(db.Integer, doc="Id of the monster on the portal")
    duration = db.Column(db.Integer, doc='Duration of the capture in seconds')
    catching_end = db.Column(sau.ArrowType(timezone=True), doc="Date of catching's end")
    type = db.Column(elements, doc='portal type')


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
