from flask import jsonify, request
from marshmallow import post_dump
from nestedworld_api.app import ma
from . import user
from ..monster import Monster

userMonster = user.namespace('monsters')

@userMonster.route('/')
class UserMonster(userMonster.Resource):

    class Schema(ma.Schema):
        print(globals())
        id = ma.Integer(dump_only=True)
        monster = ma.UrlFor("Monster")
        user = ma.UrlFor("User")
        surname = ma.String()
        experience = ma.Integer()
        level = ma.Integer()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'monsters' if many else 'monster'
            return {namespace: data}

    @userMonster.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import UserMonster

        monsters = UserMonster.query.all()
        return monsters

    @userMonster.accept(Schema())
    @userMonster.marshal_with(Schema())
    def post(self, data):
        from nestedworld_api.db import db
        from nestedworld_api.db import UserMonster

        monster = UserMonster(**data)

        db.session.add(monster)
        db.session.commit()

        return monster