from flask import jsonify, request
from marshmallow import post_dump
from nestedworld_api.app import ma
from . import api

monster = api.namespace('monsters')

@monster.route('/')
class Monster(monster.Resource):

    class Schema(ma.Schema):
        # id = ma.Integer(dump_only=True)
        name = ma.String()
        hp = ma.Float()
        attack = ma.Float()
        defense = ma.Float()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'monsters' if many else 'monster'
            return {namespace: data}

    @monster.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import Monster as DbMonster

        monsters = DbMonster.query.all()
        return monsters

    @monster.accept(Schema())
    @monster.marshal_with(Schema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import Monster as DbMonster

        monster = DbMonster.query.filter(DbMonster.name == data['name']).first()
        if monster is not None:
            api.abort(409, message='Monster already exists')

        monster = DbMonster(**data)

        db.session.add(monster)
        db.session.commit()

        return monster

