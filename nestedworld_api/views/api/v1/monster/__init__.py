from flask import jsonify, request
from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from .. import api

monsters = api.namespace('monsters')

from . import attacks

@monsters.route('/')
class Monsters(monsters.Resource):

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        name = ma.String()
        hp = ma.Float()
        attack = ma.Float()
        defense = ma.Float()
        speed = ma.Float()
        type = ma.String(validate=[OneOf(['water', 'fire', 'earth', 'electric', 'plant'])])

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'monsters' if many else 'monster'
            return {namespace: data}

    @monsters.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import Monster as DbMonster

        monsters = DbMonster.query.all()
        return monsters

    @monsters.accept(Schema())
    @monsters.marshal_with(Schema())
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

@monsters.route('/<monster_id>')
class Monster(monsters.Resource):

    class Schema(Monsters.Schema):

        class Meta:
            exclude = ('url',)

    @monsters.marshal_with(Schema())
    def get(self, monster_id):
        from nestedworld_api.db import Monster as DbMonster

        monster = DbMonster.query.get_or_404(monster_id)
        return monster
