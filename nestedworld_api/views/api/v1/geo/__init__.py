from marshmallow import post_dump
from nestedworld_api.app import ma
from .. import api


class PointField(ma.Field):

    def _serialize(self, value, attr, obj):
        from geoalchemy2.shape import to_shape
        point = to_shape(value)

        return [point.x, point.y]

places = api.namespace('places')


@places.route('/')
class Places(places.Resource):
    tags = ['geo']

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
        '''
            Retrieve places

            This request is used for retrieve the list of all the existing places.
        '''
        from nestedworld_api.db import Place as DbPlace

        places = DbPlace.query.all()
        return places


@places.route('/<place_id>')
class Place(places.Resource):
    tags = ['geo']

    class Schema(Places.Schema):

        class Meta:
            exclude = ('url',)

    @places.marshal_with(Schema())
    def get(self, place_id):
        '''
            Retrieve a place's informations

            This request is used for retrieve a specific place.
        '''
        from nestedworld_api.db import Place as DbPlace

        place = DbPlace.query.get_or_404(place_id)
        return place

    @places.accept(Schema())
    @places.marshal_with(Schema())
    def put(self, data, place_id):
        '''
            Update a place's informations.

            This request is used for update a specific place
            (Only used by the admin through the admin interface).
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Place as DbPlace

        place = DbPlace.query.get_or_404(place_id)
        conflict = DbPlace.query\
                          .filter(DbPlace.id != place_id)\
                          .filter(DbPlace.name == data['name'])\
                          .first()

        if conflict is not None:
            places.abort(400, 'A place with same name already exists')

        for (name, value) in data.items():
            setattr(place, name, value)

        db.session.commit()

        return place


@places.route('/regions')
class Regions(places.Resource):
    tags = ['geo']

    class Schema(ma.Schema):
        url = ma.UrlFor('.region', region_id='<id>')
        name = ma.String()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'regions' if many else 'region'
            return {namespace: data}

    @places.marshal_with(Schema(many=True))
    def get(self):
        '''
            Retrieve all regions

            This request is used for retrieve the list of all the existing regions.
        '''
        from nestedworld_api.db import Region as DbRegion

        regions = DbRegion.query.all()
        return regions


@places.route('/regions/<region_id>')
class Region(places.Resource):
    tags = ['geo']

    class Schema(Regions.Schema):

        class Meta:
            exclude = ('url',)

    @places.marshal_with(Schema())
    def get(self, region_id):
        '''
            Retrieve a region's informations

            This request is used for retrieve the information of a specific region.
        '''
        from nestedworld_api.db import Region as DbRegion

        region = DbRegion.query.get_or_404(region_id)
        return region

    @places.accept(Schema())
    @places.marshal_with(Schema())
    def put(self, data, region_id):
        '''
            Update a region's informations

            This request is used for update the information of a specific region
            (Only used by the admin through the admin interface).
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Region as DbRegion

        region = DbRegion.query.get_or_404(region_id)

        conflict = DbRegion.query\
                           .filter(DbRegion.id != region_id)\
                           .filter(DbRegion.name == data['name'])\
                           .first()

        if conflict is not None:
            places.abort(400, 'A region with same name already exists')

        for (name, value) in data.items():
            setattr(region, name, value)

        db.session.commit()

        return region


@places.route('/regions/<region_id>/places')
class RegionPlaces(places.Resource):
    tags = ['geo']

    @places.marshal_with(Places.Schema(many=True))
    def get(self, region_id):
        '''
            Retrieve all region's places

            This request is used for retrieve the list of places in a specific region.
        '''
        from nestedworld_api.db import Region

        region = Region.query.get_or_404(region_id)
        return region.places


from . import monsters
