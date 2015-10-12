from flask.ext.restplus import Resource
from flask.ext.restplus import fields
from . import api

monster = api.namespace('monsters', description='Monster operations')

@monster.route('/')
class Monster(Resource):

    result = monster.model('Monster', {
        'name': fields.String(required=True, description='Monster name'),
        'hp': fields.Float(description='Monster initial HP value'),
        'attack': fields.Float(description='Monster initial attack value'),
        'defense': fields.Float(description='Monster initial defense value'),
    })

    @monster.marshal_with(result, envelope='monsters')
    def get(self):
        from nestedworld_api.db import Monster

        monsters = Monster.query.all()
        return monsters
