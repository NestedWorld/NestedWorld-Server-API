from flask import jsonify, request
from marshmallow import post_dump
from nestedworld_api.app import ma
from nestedworld_api.login import login_required, current_session
from . import users
from nestedworld_api.db import Object

inventory = users.namespace('me/inventory')


@inventory.route('/')
class Inventory(inventory.Resource):

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        object = ma.String()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'inventory' if many else 'object'
            return {namespace: data}

    class InventoryResult(ma.Schema):

        class Infos(ma.Schema):
            id = ma.Integer(dump_only=True)
            url = ma.UrlFor('api.v1.objects.object', object_id='<id>')

            name = ma.String()
            description = ma.String()
            premium = ma.Boolean()
            price = ma.Integer()
            image = ma.Url()
            kind = ma.String()
            power = ma.Integer()

        id = ma.Integer(dump_only=True)
        infos = ma.Nested(Infos, attribute="object")

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'inventory' if many else 'object'
            return {namespace: data}



    @login_required
    @inventory.marshal_with(InventoryResult(many=True))
    def get(self):
        '''
            Retrieve current user's inventory

            This request is used by a user for retrieve the list
            of all objects in his inventory.
        '''
        from nestedworld_api.db import Inventory

        inventory = Inventory.query.filter(Inventory.user == current_session.user)
        return inventory

    @login_required
    @inventory.accept(Schema())
    @inventory.marshal_with(Schema())
    def post(self, data):
        '''
            Add an object in current user's inventory

            This request is used by a user for add an existing object to his inventory.
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Inventory

        choosedObject = Object.query.filter(
            Object.name == data['object']).first()
        if choosedObject is None:
            inventory.abort(400, message='Object not found')

        result = Inventory()
        result.user = current_session.user
        result.object = choosedObject

        db.session.add(result)
        db.session.commit()

        return result

@inventory.route('/<object_id>')
class ObjectInventory(inventory.Resource):

    @inventory.marshal_with(Inventory.InventoryResult())
    def get(self, object_id):
        '''
            Get a specific object in current user's inventory

            This request is use by a user for getting an existing object to his inventory
        '''

        from nestedworld_api.db import Inventory

        result = Inventory.query.filter(Inventory.id == object_id).first()
        return result

    @login_required
    def delete(self, object_id):
        '''
            Delete an object in current user's inventory

            This request is use by a user for deleting an existing object to his inventory
        '''

        from nestedworld_api.db import db
        from nestedworld_api.db import Inventory

        Inventory.query.filter(Inventory.id == object_id).delete()
        db.session.commit()
