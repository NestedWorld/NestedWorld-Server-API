import arrow
import sqlalchemy_utils as sau
from . import db


class Object(db.Model):

    __tablename__ = 'objects'

    id = db.Column(db.Integer, primary_key=True, doc='Object ID')

    name = db.Column(db.String, doc='Object name')
    premium = db.Column(db.Boolean, doc='Object is premium or not')
    price = db.Column(db.Integer, doc='Object price')
