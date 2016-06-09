import arrow
import sqlalchemy_utils as sau
from nestedworld_api.db import db
from geoalchemy2 import Geometry, Geography

#from .plant import Plant

class Object(db.Model):

    __tablename__ = 'objects'

    id = db.Column(db.Integer, primary_key=True, doc='Object ID')

    name = db.Column(db.String, doc='Object name')
    premium = db.Column(db.Boolean, doc='Object is premium or not')
    price = db.Column(db.Integer, doc='Object price')
    type = db.Column(db.String, doc='Object type')

    __mapper_args__ = {
        'polymorphic_identity': 'object',
        'polymorphic_on':type
    }

class Plant(Object):

    __tablename__ = 'plant'

    id = db.Column(db.Integer, db.ForeignKey('objects.id'), primary_key=True)
    point = db.Column(Geography('POINT'), doc='Plant geography point')

    __mapper_args__ = {
        'polymorphic_identity':'plant'
    }
