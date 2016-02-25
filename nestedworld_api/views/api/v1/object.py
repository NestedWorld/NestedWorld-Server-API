from flask import jsonify, request
from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from nestedworld_api.login import login_required
from . import api

Object = api.namespace('objects')

@Object.route('/')
class Object(Object.Resource):

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        name = ma.String()
        premium = ma.Boolean()
        price = ma.Integer()


        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'Objects' if many else 'Object'
            return {namespace: data}

    @Object.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import Object as DbObject

        Objects = DbObject.query.all()
        return Objects

    @login_required
    @Object.accept(Schema())
    @Object.marshal_with(Schema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import Object as DbObject

        Object = DbObject.query.filter(DbObject.name == data['name']).first()
        if Object is not None:
            api.abort(409, message='Object already exists')

        Object = DbObject(**data)

        db.session.add(Object)
        db.session.commit()

        return Object
