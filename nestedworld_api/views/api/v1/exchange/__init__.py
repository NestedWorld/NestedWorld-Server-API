from flask import jsonify, request
from marshmallow import post_dump
from nestedworld_api.app import ma
from .. import api

exchanges = api.namespace("exchange")

@exchanges.route('/')
class Exchanges(exchanges.Resource):
    tags = ['exchanges']

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        monster_sended = ma.Integer()
        umonster_sended = ma.Integer()
        monster_asked = ma.Integer()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'exchanges' if many else 'exchange'
            return {namespace: data}

    @exchanges.marshal_with(Schema(many=True))
    def get(self):
        '''
            Retrieve a list of all existing exchanges

            This request is used for retrieve the list of all the existing exchange.
        '''
        from nestedworld_api.db import Exchange as DbExchange

        exhanges = DbExchange.query.all()
        return exhanges

    @exchanges.accept(Schema())
    @exchanges.marshal_with(Schema())
    def post(self, data):
        '''http://marshmallow.readthedocs.io/en/latest/api_reference.html
            Create a new exchange

            This request is used by a user to create a new exchange
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Exchange as DbExchange
        from nestedworld_api.db import UserMonster as DbUserMonster
        from nestedworld_api.db import Monster as DbMonster

        monster = DbExchange.query.filter(DbExchange.umonster_sended == data['umonster_sended']).first()
        if monster is not None:
            api.abort(409, message='Monster already in exchange')
        monster = DbUserMonster.query.filter(DbUserMonster.id == data['umonster_sended']).first()
        if monster is None:
            api.abort(409, message='User Monster doesn\'t exist')
        monster = DbMonster.query.filter(DbMonster.id == data['monster_sended']).first()
        if monster is None:
            api.abort(409, message='Monster sended doesn\'t exist')
        monster = DbMonster.query.filter(DbMonster.id == data['monster_asked']).first()
        if monster is None:
            api.abort(409, message='Monster asked doesn\'t exist')

        exchange = DbExchange(**data)
        db.session.add(exchange)
        db.session.commit()
        return exchange

@exchanges.route('/<exchange_id>')
class Exchange(exchanges.Resource):
    tags = ['exchanges']

    class Schema(ma.Schema):
        sended = ma.Integer(default=True)

    @exchanges.accept(Schema())
    def post(self, data, exchange_id):
        '''
            Make the Exchange

            This resquest is used by a user for making an exchange
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Exchange as DbExchange
        from nestedworld_api.db import User as DbUser
        from nestedworld_api.db import UserMonster as DbUserMonster

        exchange = DbExchange.query.get_or_404(exchange_id)
        monster = DbUserMonster.query.filter(DbUserMonster.id == data['sended']).first().delete()
        if monster is None:
            api.abort(409, message='User Monster doesn\'t exist')
        opp_monster = DbUserMonster.query.filter(DbUserMonster.id == exchange.umonster_sended).first()
        user = monster.user
        opp = opp_monster.user
        monster.user = opp
        opp_monster.user = user
        db.session.add(monster)
        db.session.add(opp_monster)
        db.session.commit()
        return {"message" : "ok"}
