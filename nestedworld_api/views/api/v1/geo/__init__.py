from marshmallow import post_dump
from nestedworld_api.app import ma
from marshmallow.validate import OneOf
from geoalchemy2.shape import to_shape
from .. import api


class PointField(ma.Field):

    def _serialize(self, value, attr, obj):
        point = to_shape(value)

        return [point.x, point.y]

portals = api.namespace('geo')


@portals.route('/portals')
class Portals(portals.Resource):
    tags = ['geo']

    class Schema(ma.Schema):
        id = ma.Integer(dump_only=True)
        url = ma.UrlFor('.portal', portal_id='<id>')
        name = ma.String()
        position = PointField(attribute='point')
        type = ma.String(validate=[OneOf(['water', 'fire', 'earth', 'electric', 'plant'])])
        created = ma.DateTime(dump_only=True)
        captured = ma.DateTime()
        captured_by = ma.Integer()
        umonster_on = ma.Integer()
        monster_on = ma.Integer()
        catching_end = ma.DateTime()
        duration = ma.Integer()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'portals' if many else 'portal'
            return {namespace: data}

    @portals.marshal_with(Schema(many=True))
    def get(self):
        '''
            Retrieve portals

            This request is used for retrieve the list of all the existing portals.
        '''
        from nestedworld_api.db import Portal as DbPortal

        portals = DbPortal.query.all()
        return portals


@portals.route('/portals/<portal_id>/')
class Portal(portals.Resource):
    tags = ['geo']

    class Schema(Portals.Schema):

        class Meta:
            exclude = ('url',)

    @portals.marshal_with(Schema())
    def get(self, portal_id):
        '''
            Retrieve a portal's informations

            This request is used for retrieve a specific portal.
        '''
        from nestedworld_api.db import Portal as DbPortal

        portal = DbPortal.query.get_or_404(portal_id)
        return portal

    @portals.accept(Schema())
    @portals.marshal_with(Schema())
    def put(self, data, portal_id):
        '''
            Update a portal's informations.

            This request is used for update a specific portal
            (Only used by the admin through the admin interface).
        '''
        from nestedworld_api.db import db
        from nestedworld_api.db import Portal as DbPortal

        portal = DbPortal.query.get_or_404(portal_id)
        conflict = DbPortal.query\
                           .filter(DbPortal.id != portal_id)\
                           .filter(DbPortal.name == data['name'])\
                           .first()

        if conflict is not None:
            portals.abort(400, 'A portal with same name already exists')

        for (name, value) in data.items():
            setattr(portal, name, value)

        db.session.commit()

        return portal


@portals.route('/portals/<float:long>/<float:lat>')
class PortalsNear(portals.Resource):

    class Schema(Portals.Schema):

        distance = ma.Float()

        class Meta:
            exclude = ('url',)

    @portals.marshal_with(Schema(many=True))
    def get(self, long, lat):
        '''
            Retrieve portals near the specified location
        '''
        from geoalchemy2 import Geography
        from geoalchemy2 import functions, shape
        from nestedworld_api.db import Portal as DbPortal
        from shapely.geometry import Point
        from sqlalchemy import cast

        point = shape.from_shape(Point(lat, long))
        distance = functions.ST_Distance(DbPortal.point, point)\
            .label('distance')
        portals = DbPortal.query\
            .add_columns(distance)\
            .filter(distance < 250)\
            .order_by(distance)\
            .all()
        for (portal, distance) in portals:
            portal.distance = distance

        return (entry[0] for entry in portals)


@portals.route('/regions/')
class Regions(portals.Resource):
    tags = ['geo']

    class Schema(ma.Schema):
        url = ma.UrlFor('.region', region_id='<id>')
        name = ma.String()

        @post_dump(pass_many=True)
        def add_envelope(self, data, many):
            namespace = 'regions' if many else 'region'
            return {namespace: data}

    @portals.marshal_with(Schema(many=True))
    def get(self):
        '''
            Retrieve all regions

            This request is used for retrieve the list of all the existing regions.
        '''
        from nestedworld_api.db import Region as DbRegion

        regions = DbRegion.query.all()
        return regions


@portals.route('/regions/<region_id>/')
class Region(portals.Resource):
    tags = ['geo']

    class Schema(Regions.Schema):

        class Meta:
            exclude = ('url',)

    @portals.marshal_with(Schema())
    def get(self, region_id):
        '''
            Retrieve a region's informations

            This request is used for retrieve the information of a specific region.
        '''
        from nestedworld_api.db import Region as DbRegion

        region = DbRegion.query.get_or_404(region_id)
        return region

    @portals.accept(Schema())
    @portals.marshal_with(Schema())
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
            portals.abort(400, 'A region with same name already exists')

        for (name, value) in data.items():
            setattr(region, name, value)

        db.session.commit()

        return region


@portals.route('/regions/<region_id>/portals')
class RegionPlaces(portals.Resource):
    tags = ['geo']

    @portals.marshal_with(Portals.Schema(many=True))
    def get(self, region_id):
        '''
            Retrieve all region's portals

            This request is used for retrieve the list of portals in a specific region.
        '''
        from nestedworld_api.db import Region

        region = Region.query.get_or_404(region_id)
        return region.portals
