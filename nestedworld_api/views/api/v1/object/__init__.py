from flask import jsonify, request
from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from nestedworld_api.login import login_required
from .. import api

from . import plant

object = api.namespace('objects')


@object.route('/')
class Object(object.Resource):

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        name = ma.String()
        premium = ma.Boolean()
        price = ma.Integer()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'Objects' if many else 'Object'
            return {namespace: data}

    @object.marshal_with(Schema(many=True))
    def get(self):
        '''
            Retrieve all objects

            This request is used for retrieve the list of all the existing objects.
        '''
        from nestedworld_api.db import Object as DbObject

        Objects = DbObject.query.all()
        return Objects

    @login_required
    @object.accept(Schema())
    @object.marshal_with(Schema())
    def post(self, data):
        '''
            Create a new object

            This request is used for create a new object
            (Only used by the admin through the admin interface).
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Object as DbObject

        Object = DbObject.query.filter(DbObject.name == data['name']).first()
        if Object is not None:
            object.abort(409, message='Object already exists')

        Object = DbObject(**data)

        db.session.add(Object)
        db.session.commit()

        return Object
