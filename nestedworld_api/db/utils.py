from . import db

def IDColumn(**kwargs):
    return db.Column(db.Integer, primary_key=True, **kwargs)
