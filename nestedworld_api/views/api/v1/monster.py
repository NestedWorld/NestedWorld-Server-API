from flask.ext.restplus import Resource
from flask.ext.restplus import fields
from . import api

monster = api.namespace('monsters', description='Monster operations')

@monster.route('/')
class Monster(Resource):

    parser = monster.parser()
    parser.add_argument(
        'name', type=str, required=True, help='Monster name', location='form')
    parser.add_argument(
        'hp', type=float, required=True, help='Monster initial HP value', location='form')
    parser.add_argument(
        'attack', type=float, required=True, help='Monster initial attack value', location='form')
    parser.add_argument(
        'defense', type=float, required=True, help='Monster initial defense value', location='form')

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

    @monster.doc(parser=parser)
    @monster.marshal_with(result, envelope='monsters')
    def post(self):
        from nestedworld_api.db import db
        from nestedworld_api.db import Monster as DbMonster

        args = Monster.parser.parse_args()

        monster = DbMonster.query.filter(DbMonster.name == args.name).first()
        if monster is not None:
            auth.abort(409, 'Monster already exists')

        monster = DbMonster()
        monster.name = args.name
        monster.hp = args.hp
        monster.attack = args.attack
        monster.defense = args.defense

        db.session.add(monster)
        db.session.commit()

        return monster
