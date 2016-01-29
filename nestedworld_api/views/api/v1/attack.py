from flask import jsonify, request
from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from . import api

attack = api.namespace('attacks')

@attack.route('/')
class Attack(attack.Resource):

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        name = ma.String()
        type = ma.String(validate=[OneOf(['attack', 'attacksp', 'defense', 'defensesp'])])


        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'attacks' if many else 'attack'
            return {namespace: data}

    @attack.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import Attack as DbAttack

        attacks = DbAttack.query.all()
        return attacks

    @attack.accept(Schema())
    @attack.marshal_with(Schema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import Attack as DbAttack

        attack = DbAttack.query.filter(DbAttack.name == data['name']).first()
        if attack is not None:
            api.abort(409, message='Attack already exists')

        attack = DbAttack(**data)

        db.session.add(attack)
        db.session.commit()

        return attack
