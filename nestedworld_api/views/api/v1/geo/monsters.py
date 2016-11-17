from marshmallow import post_dump
from nestedworld_api.app import ma
from . import portals


@portals.route('/portals/<int:portal_id>/monsters')
class PortalMonsters(portals.Resource):
    tags = ['geo']

    class Schema(ma.Schema):

        class Infos(ma.Schema):
            id = ma.Integer(dump_only=True)
            url = ma.UrlFor('api.v1.monsters.monster', monster_id='<id>')

            name = ma.String()
            hp = ma.Float()
            attack = ma.Float()
            defense = ma.Float()

        infos = ma.Nested(Infos, attribute='monster')

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'monsters' if many else 'monster'
            return {namespace: data}

    @portals.marshal_with(Schema(many=True))
    def get(self, portal_id):
        '''
            Retrieve all portal's monsters

            This request is used for retrieve the list of all the existing monsters in a specific portal.
        '''
        from nestedworld_api.db import PortalMonster
        from sqlalchemy.orm import joinedload

        monsters = PortalMonster.query\
                                .filter(PortalMonster.portal_id == portal_id)\
                                .options(joinedload('monster'))\
                                .all()
        return monsters


@portals.route('/regions/<region_id>/monsters')
class RegionMonsters(portals.Resource):
    tags = ['geo']

    class Schema(ma.Schema):

        class Infos(ma.Schema):
            id = ma.Integer(dump_only=True)
            url = ma.UrlFor('api.v1.monsters.monster', monster_id='<id>')

            name = ma.String()
            hp = ma.Float()
            attack = ma.Float()
            defense = ma.Float()

        class Interval(ma.Schema):

            lower = ma.Integer()
            upper = ma.Integer()

        infos = ma.Nested(Infos, attribute='monster')
        ratio = ma.Float()
        level = ma.Nested(Interval)

    @portals.marshal_with(Schema(many=True))
    def get(self, region_id):
        '''
            Retrieve all region's monsters

            This request is used for retrieve the list of all the monsters in a specific region.
        '''
        from nestedworld_api.db import RegionMonster
        from sqlalchemy.orm import joinedload

        monsters = RegionMonster.query\
                                .filter(RegionMonster.region_id == region_id)\
                                .options(joinedload('monster'))\
                                .all()
        return monsters
