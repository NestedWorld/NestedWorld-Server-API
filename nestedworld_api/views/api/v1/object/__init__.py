from flask import jsonify, request
from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from nestedworld_api.login import login_required
from .. import api

objects = api.namespace('objects')

@objects.route('/')
class Objects(objects.Resource):

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        name = ma.String()
        description = ma.String()
        premium = ma.Boolean()
        price = ma.Integer()
        image = ma.Url()
        kind = ma.String()
        power = ma.Integer()


        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'Objects' if many else 'Object'
            return {namespace: data}

    @objects.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import Object as DbObject

        Objects = DbObject.query.all()
        return Objects

    @login_required
    @objects.accept(Schema())
    @objects.marshal_with(Schema())
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

@objects.route('/<object_id>')
class Object(objects.Resource):

    @objects.marshal_with(Objects.Schema())
    def get(self, object_id):
        from nestedworld_api.db import Object as DbObject

        Object = DbObject.query.filter(DbObject.id == object_id).first()
        return Object

    @login_required
    def delete(self, object_id):
        from nestedworld_api.db import db
        from nestedworld_api.db import Object as DbObject

        DbObject.query.filter(DbObject.id == object_id).delete()
        db.session.commit()
