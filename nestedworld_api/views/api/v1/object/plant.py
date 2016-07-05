from flask import jsonify, request
from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from nestedworld_api.login import login_required
from . import api

plant = api.namespace('plants')

@plant.route('/')
class Plant(plant.Resource):

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        name = ma.String()
        premium = ma.Boolean()
        price = ma.Integer()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'Plants' if many else 'Plant'
            return {namespace: data}

    @plant.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import Plant as DbPlant

        Plants = DbPlant.query.all()
        return Plants

    @login_required
    @plant.accept(Schema())
    @plant.marshal_with(Schema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import Plant as DbPlant

        Plant = DbPlant.query.filter(DbPlant.name == data['name']).first()
        if Plant is not None:
            plant.abort(409, message='Plant already exists')

        Plant = DbPlant(**data)

        db.session.add(Plant)
        db.session.commit()

        return Plant
