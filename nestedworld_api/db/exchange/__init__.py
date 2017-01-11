from .. import db
from ..utils import IDColumn

class Exchange(db.Model):

    __tablename__ ='exchanges'

    id = IDColumn(doc ="Exchange ID")
    monster_sended = db.Column(db.Integer, doc="monster sended by the player")
    umonster_sended = db.Column(db.Integer, doc="user monster sended by the player")
    monster_asked = db.Column(db.Integer, doc="Monster asked for the exchange")
