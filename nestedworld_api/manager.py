from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from .app import app
from .db import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def resetdb():
    '''
        Reset the database.
    '''
    from .db import db, fixtures
    from .db import Application, User, Session

    db.drop_all()
    db.create_all()
    fixtures.reset_db()
    db.session.commit()

@manager.command
def reset_password(email):
    from nestedworld_api.app import app
    from nestedworld_api.db import db
    from nestedworld_api.db import User, PasswordResetRequest
    from nestedworld_api.mail import TemplatedMessage

    user = User.query.filter(
        User.email == email, User.is_active == True).first()
    if user is None:
        print('User not found.')
        return

    request = PasswordResetRequest(user=user)
    db.session.add(request)
    db.session.commit()

    message = TemplatedMessage('mail/password_reset.txt', token=request.token)
    message.add_recipient(user.email)
    message.send()

    print('Done.')

@manager.command
def import_monsters():
    import requests
    from nestedworld_api.db import db
    from nestedworld_api.db import Monster

    print('Fetching data...')
    r = requests.get('http://pokeapi.co/api/v1/pokemon/?limit=42')
    objects = r.json()['objects']

    print('Importing data...')
    monsters = []
    for obj in objects:
        monster = Monster()
        monster.name = obj['name']
        monster.hp = obj['hp']
        monster.attack = obj['attack']
        monster.defense = obj['defense']

        monsters.append(monster)

    db.session.bulk_save_objects(monsters)
    db.session.commit()

@manager.command
def import_places():
    import requests
    from collections import namedtuple
    from geoalchemy2.shape import from_shape
    from nestedworld_api.db import db
    from nestedworld_api.db import Place, Region
    from nestedworld_api.db import User
    from shapely.geometry import Point
    from pprint import pprint
    # from tqdm import tqdm

    admin = db.session.query(User)\
                      .filter(User.email == 'kokakiwi@kokakiwi.net')\
                      .first()

    def get_polygon(rel_id):
        r = requests.get('http://polygons.openstreetmap.fr/get_wkt.py?id=%d&params=0' % (int(rel_id)))
        data = r.text

        return data

    BASE_URL = 'http://overpass-api.de/api/interpreter'

    def query_overpass(query):
        payload = {'data': '[out:json];%s' % (query)}
        r = requests.post(BASE_URL, data=payload, headers={'Accept-Charset': 'utf-8;q=0.7,*;q=0.7'})

        return r.json()['elements']

    print('Querying...')
    r = query_overpass('area["name:en"="Seoul"];out;node(area)[name];out 3000 body;')
    city = r[0]
    points = r[1:]

    # City
    city_rel_id = int(city['id'] - 3.6e9)
    city_polygon = get_polygon(city_rel_id)

    city_tags = city['tags']
    city_name = city_tags.get('name:en', city_tags.get('name'))

    print('Importing %s...' % (city_name))
    city_region = Region(name=city_name, zone=city_polygon)
    db.session.add(city_region)

    # Points
    for point in points:
        point_data = from_shape(Point(point['lon'], point['lat']))

        point_tags = point['tags']
        point_name = point_tags.get('name:en', point_tags.get('name'))

        print('Importing %s...' % (point_name))
        point_place = Place(name=point_name, author=admin, point=point_data)
        db.session.add(point_place)

    db.session.commit()
