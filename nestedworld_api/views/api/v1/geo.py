from marshmallow import post_dump
from nestedworld_api.app import ma
from . import api

class PointField(ma.Field):

    def _serialize(self, value, attr, obj):
        from geoalchemy2.shape import to_shape
        point = to_shape(value)

        return [point.x, point.y]

places = api.namespace('places')

@places.route('/')
class Places(places.Resource):

    class Schema(ma.Schema):
        url = ma.UrlFor('.place', place_id='<id>')
        name = ma.String()
        position = PointField(attribute='point')

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'places' if many else 'place'
            return {namespace: data}

    @places.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import Place as DbPlace

        places = DbPlace.query.all()
        return places

@places.route('/<place_id>')
class Place(places.Resource):

    class Schema(Places.Schema):

        class Meta:
            exclude = ('url',)

    @places.marshal_with(Schema())
    def get(self, place_id):
        from nestedworld_api.db import Place as DbPlace

        place = DbPlace.query.get_or_404(place_id)
        return place

@places.route('/regions')
class Regions(places.Resource):

    class Schema(ma.Schema):
        url = ma.UrlFor('.region', region_id='<id>')
        name = ma.String()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'regions' if many else 'region'
            return {namespace: data}

    @places.marshal_with(Schema(many=True))
    def get(self):
        from nestedworld_api.db import Region as DbRegion

        regions = DbRegion.query.all()
        return regions

@places.route('/regions/<region_id>')
class Region(places.Resource):

    class Schema(Regions.Schema):

        places = ma.List(ma.Nested(Places.Schema))

        class Meta:
            exclude = ('url',)

    @places.marshal_with(Schema())
    def get(self, region_id):
        from nestedworld_api.db import Region as DbRegion

        region = DbRegion.query.get_or_404(region_id)
        return region
