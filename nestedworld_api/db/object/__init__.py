import arrow
import sqlalchemy_utils as sau
from nestedworld_api.db import db
from geoalchemy2 import Geometry, Geography

#from .plant import Plant

class Object(db.Model):

    __tablename__ = 'objects'

    id = db.Column(db.Integer, primary_key=True, doc='Object ID')

    name = db.Column(db.String, doc='Object name')
    description = db.Column(db.String, doc='Object description')
    premium = db.Column(db.Boolean, doc='Object is premium or not')
    price = db.Column(db.Integer, doc='Object price')
    type = db.Column(db.String, doc='Object type')
    image = db.Column(db.String(2000), nullable=True, doc='Object image')
    kind = db.Column(db.Enum('heal', 'att-up', 'attsp-up', 'def-up', 'defsp-up',
                             name='object_kind'), doc='Object kind')
    power = db.Column(db.Integer, doc='Object power')

    __mapper_args__ = {
        'polymorphic_identity': 'object',
        'polymorphic_on':type
    }

class Plant(Object):

    __tablename__ = 'plant'

    id = db.Column(db.Integer, db.ForeignKey('objects.id', ondelete="CASCADE"), primary_key=True, doc='Plant ID')
    point = db.Column(Geography('POINT'), doc='Plant geography point')

    __mapper_args__ = {
        'polymorphic_identity':'plant'
    }
