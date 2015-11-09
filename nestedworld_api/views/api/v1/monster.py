from flask.ext.restplus import Resource
from flask.ext.restplus import fields
from flask import jsonify, request
from marshmallow import Schema, fields as marshmallowFields
from . import api

monster = api.namespace('monsters', description='Monster operations')

@monster.route('/')
class Monster(Resource):

    class MonsterSchema(Schema):
        name = marshmallowFields.String();
        hp = marshmallowFields.Float();
        attack = marshmallowFields.Float();
        defense = marshmallowFields.Float();

    monster_schema = MonsterSchema()
    monsters_schema = MonsterSchema(many=True)

    def get(self):
        from nestedworld_api.db import Monster as DbMonster

        monsters = DbMonster.query.all()
        result = self.monsters_schema.dump(monsters);
        return jsonify({'monsters': result.data})

    def post(self):
        from nestedworld_api.db import db
        from nestedworld_api.db import Monster as DbMonster

        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400
        data, errors = self.monster_schema.load(json_data)
        if errors:
            return jsonify(errors), 422

        monster = DbMonster.query.filter(DbMonster.name == data.name).first()
        if monster is not None:
            auth.abort(409, 'Monster already exists')

        monster = DbMonster()
        monster.name = data.name
        monster.hp = data.hp
        monster.attack = data.attack
        monster.defense = data.defense

        db.session.add(monster)
        db.session.commit()

        return monster

