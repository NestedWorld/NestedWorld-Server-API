from flask import jsonify, request
from marshmallow import post_dump
from nestedworld_api.app import ma
from nestedworld_api.login import login_required, current_session
from . import monsters
from nestedworld_api.db import Attack
from nestedworld_api.db import Monster

monster_attacks = monsters.namespace('attacks')


@monsters.route('/<monster_id>/attacks')
class MonsterAttack(monster_attacks.Resource):
    tags = ['monsters']

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        attack = ma.String()
        monster = ma.String()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'attacks' if many else 'attack'
            return {namespace: data}

    @monster_attacks.marshal_with(Schema(many=True))
    def get(self, monster_id):
        from nestedworld_api.db import MonsterAttack

        attacks = MonsterAttack.query.all()
        return attacks

    class PostSchema(ma.Schema):
        attack = ma.String()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'attacks' if many else 'attack'
            return {namespace: data}

    @monster_attacks.accept(PostSchema())
    @monster_attacks.marshal_with(Schema())
    def post(self, monster_id, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import MonsterAttack

        choosedAttack = Attack.query.filter(
            Attack.name == data['attack']).first()
        if choosedAttack is None:
            monster_attacks.abort(400, message='Attack not found')

        choosedMonster = Monster.query.get_or_404(monster_id)

        attack = MonsterAttack()
        attack.monster = choosedMonster
        attack.attack = choosedAttack

        db.session.add(attack)
        db.session.commit()

        return attack
