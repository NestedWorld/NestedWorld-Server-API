from flask import jsonify, request
from marshmallow import post_dump
from marshmallow.validate import OneOf
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

    class AttackResult(ma.Schema):

        class Infos(ma.Schema):
            id = ma.Integer(dump_only=True)
            url = ma.UrlFor('api.v1.attacks.attack', attack_id='<id>')

            name = ma.String()
            type = ma.String(validate=[OneOf(['attack', 'attacksp', 'defense', 'defensesp'])])

        id = ma.Integer(dump_only=True)
        infos = ma.Nested(Infos, attribute="attack")

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'attacks' if many else 'attack'
            return {namespace: data}

    @monster_attacks.marshal_with(AttackResult(many=True))
    def get(self, monster_id):
        '''
            Retrieve a monster's attacks

            This request is used for retrieve the attacks of a specific monster.
        '''
        from nestedworld_api.db import MonsterAttack

        attacks = MonsterAttack.query.filter(MonsterAttack.monster == Monster.query.filter(Monster.id == monster_id).first());
        return attacks

    @monster_attacks.accept(Schema())
    @monster_attacks.marshal_with(Schema())
    def post(self, monster_id, data):
        '''
            Add an attack to a monster

            This request is used for link an existing attack to an existing monster
            (Only used by the admin through the admin interface).
        '''
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
