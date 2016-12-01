from flask import jsonify, request
from marshmallow import post_dump
from nestedworld_api.app import ma
from nestedworld_api.db import Monster
from nestedworld_api.db import User
from nestedworld_api.login import login_required, current_session
from . import users

user_monsters = users.namespace('monsters')


@user_monsters.route('/')
class UserMonsters(user_monsters.Resource):
    tags = ['users']

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        monster = ma.String()
        surname = ma.String()
        experience = ma.Integer()
        level = ma.Integer()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'monsters' if many else 'monster'
            return {namespace: data}

    class MonsterResult(ma.Schema):

        class Infos(ma.Schema):
            id = ma.Integer(dump_only=True)
            url = ma.UrlFor('api.v1.monsters.monster', monster_id='<id>')

            name = ma.String()
            hp = ma.Float()
            attack = ma.Float()
            defense = ma.Float()
            base_sprite = ma.Url()


        id = ma.Integer(dump_only=True)
        infos = ma.Nested(Infos, attribute='monster')
        surname = ma.String()
        experience = ma.Integer()
        level = ma.Integer()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'monsters' if many else 'monster'
            return {namespace: data}

    @login_required
    @user_monsters.marshal_with(MonsterResult(many=True))
    def get(self):
        '''
            Retrieve current user's monsters list

            This request is used by a user for retrieve his own monsters list.
        '''
        from nestedworld_api.db import UserMonster as DbUserMonster

        monsters = DbUserMonster.query.filter(DbUserMonster.user_id == current_session.user.id);
        return monsters

    @login_required
    @user_monsters.accept(Schema())
    @user_monsters.marshal_with(Schema())
    def post(self, data):
        '''
            Add a monster to current user's monsters list.

            This request is used by a user for add an existing monster to his monsters list.
        '''
        from nestedworld_api.db import db

        choosedMonster = Monster.query.filter(
            Monster.name == data['monster']).first()
        if choosedMonster is None:
            user_monsters.abort(400, message='Monster not found')

        monster = UserMonsters()
        monster.user = current_session.user
        monster.monster = choosedMonster
        monster.surname = data['surname']
        monster.experience = data['experience']
        monster.level = data['level']

        db.session.add(monster)
        db.session.commit()

        return monster

@user_monsters.route('/<monster_id>/')
class UserMonster(user_monsters.Resource):

    @login_required
    @user_monsters.marshal_with(UserMonsters.MonsterResult())
    def get(self, monster_id):
        '''
            Retrieve a specific monster of the user

            This request is used by a user for retrieve his own monster.
        '''
        from nestedworld_api.db import UserMonster as DbUserMonster

        monster = DbUserMonster.query.filter(DbUserMonster.user_id == current_session.user.id, DbUserMonster.id == monster_id).first()
        return monster


    @login_required
    def delete(self, monster_id):
        '''
            Delete a monster to current user's monsters list.

            This request is used by a user for deleting an existing monster to his monsters list.
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import UserMonster as DbUserMonster

        DbUserMonster.query.filter(DbUserMonster.id == monster_id, DbUserMonster.user_id == current_session.user.id).delete()
        db.session.commit()
        return {"message":"ok"}
