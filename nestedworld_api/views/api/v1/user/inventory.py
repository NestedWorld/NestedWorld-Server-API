from flask import jsonify, request
from marshmallow import post_dump
from nestedworld_api.app import ma
from nestedworld_api.login import login_required, current_session
from . import user
from nestedworld_api.db import Object

inventory = user.namespace('inventory')

@inventory.route('/')
class Inventory(inventory.Resource):

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        object = ma.String()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'inventory'
            return {namespace: data}

    @login_required
    @inventory.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import Inventory

        inventory = Inventory.query.all()
        return inventory

    @login_required
    @inventory.accept(Schema())
    @inventory.marshal_with(Schema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import Inventory

        choosedObject = Object.query.filter(
            Object.name == data['object']).first()
        if choosedObject is None:
            inventory.abort(400, message='Object not found')

        result = Inventory()
        result.user = current_session.user
        result.object = choosedObject

        db.session.add(inventory)
        db.session.commit()

        return result
