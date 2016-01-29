from flask import jsonify, request
from marshmallow import post_dump
from nestedworld_api.app import ma
from nestedworld_api.login import login_required, current_session
from . import user
from nestedworld_api.db import Monster

user_monsters = user.namespace('monsters')


@user_monsters.route('/')
class UserMonster(user_monsters.Resource):

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        monster = ma.String()
        user = ma.String()
        surname = ma.String()
        experience = ma.Integer()
        level = ma.Integer()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'monsters' if many else 'monster'
            return {namespace: data}

    @login_required
    @user_monsters.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import UserMonster

        monsters = UserMonster.query.all()
        return monsters

    @login_required
    @user_monsters.accept(Schema())
    @user_monsters.marshal_with(Schema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import UserMonster

        choosedMonster = Monster.query.filter(
            Monster.name == data['monster']).first()
        if choosedMonster is None:
            auth.abort(400, message='Monster not found')

        monster = UserMonster()
        monster.user = current_session.user
        monster.monster = choosedMonster
        monster.surname = data['surname']
        monster.experience = data['experience']
        monster.level = data['level']

        db.session.add(monster)
        db.session.commit()

        return monster
