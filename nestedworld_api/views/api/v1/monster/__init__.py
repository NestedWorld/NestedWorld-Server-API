from flask import jsonify, request
from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from .. import api

monsters = api.namespace('monsters')

from . import attacks


@monsters.route('/')
class Monsters(monsters.Resource):
    tags = ['monsters']

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
        '''
            Retrieve a list of all existing monsters

            This request is used for retrieve the list of all the existing monster.
        '''
        from nestedworld_api.db import Monster as DbMonster

        monsters = DbMonster.query.all()
        return monsters

    @monsters.accept(Schema())
    @monsters.marshal_with(Schema())
    def post(self, data):
        '''
            Create a new monster

            This request is used for create a new monster (Only used by the admin through the admin interface).
        '''
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
    tags = ['monsters']

    class Schema(Monsters.Schema):

        class Meta:
            exclude = ('url',)

    @monsters.marshal_with(Schema())
    def get(self, monster_id):
        '''
            Retrieve a monster's informations

            This request is used for retrieve the information of a specific monster.
        '''
        from nestedworld_api.db import Monster as DbMonster

        monster = DbMonster.query.get_or_404(monster_id)
        return monster

    @monsters.accept(Schema())
    @monsters.marshal_with(Schema())
    def put(self, data, monster_id):
        '''
            Update a monster's informations

            This request is used for update the information of a specific monster
            (Only used by the admin through the admin interface).
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Monster as DbMonster

        monster = DbMonster.query.get_or_404(monster_id)

        conflict = DbMonster.query\
                            .filter(DbMonster.id != monster_id)\
                            .filter(DbMonster.name == data['name'])\
                            .first()

        if conflict is not None:
            monsters.abort(400, 'An monster with same name already exists')

        for (name, value) in data.items():
            setattr(monster, name, value)

        db.session.commit()

        return monster

    @monsters.marshal_with(Schema())
    def delete(self, monster_id):
        '''
            Delete a monster

            This request is userd for delete the information of a specific monster
            (Only user by the admin through the admin interface).
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Monster as DbMonster

        monster = DbMonster.query.get_or_404(monster_id)

        db.session.delete(monster)
        db.session.commit()

        return monster
