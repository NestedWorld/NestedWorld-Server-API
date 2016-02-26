from nestedworld_api.app import ma
from . import places

@places.route('/<place_id>/monsters')
class PlaceMonsters(places.Resource):
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

    @places.marshal_with(Schema(many=True))
    def get(self, place_id):
        from nestedworld_api.db import PlaceMonster
        from sqlalchemy.orm import joinedload

        monsters = PlaceMonster.query\
                                .filter(PlaceMonster.place_id == place_id)\
                                .options(joinedload('monster'))\
                                .all()
        return monsters


@places.route('/regions/<region_id>/monsters')
class RegionMonsters(places.Resource):
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

    @places.marshal_with(Schema(many=True))
    def get(self, region_id):
        from nestedworld_api.db import RegionMonster
        from sqlalchemy.orm import joinedload

        monsters = RegionMonster.query\
                                .filter(RegionMonster.region_id == region_id)\
                                .options(joinedload('monster'))\
                                .all()
        return monsters
