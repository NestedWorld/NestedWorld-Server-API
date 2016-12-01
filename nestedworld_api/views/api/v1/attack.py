from flask import jsonify, request
from marshmallow import post_dump
from marshmallow.validate import OneOf
from nestedworld_api.app import ma
from nestedworld_api.login import login_required
from . import api

attacks = api.namespace('attacks')


@attacks.route('/')
class Attacks(attacks.Resource):
    tags = ['attacks']

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        name = ma.String()
        type = ma.String(validate=[OneOf(['attack', 'attacksp', 'defense', 'defensesp'])])
        sprite = ma.Url()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'attacks' if many else 'attack'
            return {namespace: data}

    @attacks.marshal_with(Schema(many=True))
    def get(self):
        '''
            Retrieve all attacks

            This request is used for retrieve all the existing attacks (linked or not to a monster).
        '''
        from nestedworld_api.db import Attack as DbAttack

        attacks = DbAttack.query.all()
        return attacks

    @login_required
    @attacks.accept(Schema())
    @attacks.marshal_with(Schema())
    def post(self, data):
        '''
            Add a new attack

            This request is used for create a new attack that will not be linked to any existing monster
            (Only used by the admin through the admin interface).
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Attack as DbAttack

        attack = DbAttack.query.filter(DbAttack.name == data['name']).first()
        if attack is not None:
            api.abort(409, message='Attack already exists')

        attack = DbAttack(**data)

        db.session.add(attack)
        db.session.commit()

        return attack


@attacks.route('/<attack_id>')
class Attack(attacks.Resource):
    tags = ['attacks']

    class Schema(Attacks.Schema):

        class Meta:
            exclude = ('url',)

    @attacks.marshal_with(Schema())
    def get(self, attack_id):
        '''
            Retrieve an attack's informations

            This request is used for retrieve the information of a specific attack.
        '''
        from nestedworld_api.db import Attack as DbAttack

        attack = DbAttack.query.get_or_404(attack_id)
        return attack

    @login_required
    @attacks.accept(Schema())
    @attacks.marshal_with(Schema())
    def put(self, data, attack_id):
        '''
            Update an attack's informations

            This request is used for update the information of a specific attack
            (Only used by the admin through the admin interface).
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Attack as DbAttack

        attack = DbAttack.query.get_or_404(attack_id)

        if 'name' in data:
            conflict = DbAttack.query\
                               .filter(DbAttack.id != attack_id)\
                               .filter(DbAttack.name == data['name'])\
                               .first()

            if conflict is not None:
                attacks.abort(400, 'An attack with same name already exists')

        for (name, value) in data.items():
            setattr(attack, name, value)

        db.session.commit()

        return attack

    @login_required
    def delete(self, attack_id):
        '''
            Delete an attack

            This request is used for delete a specific attack
            (Only used by the admin through the admin interface).
        '''

        from nestedworld_api.db import db
        from nestedworld_api.db import Attack as DbAttack

        DbAttack.query.filter(DbAttack.id == attack_id).delete()
        db.session.commit()
        return {"message":"ok"}
