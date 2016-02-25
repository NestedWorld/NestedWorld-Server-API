import arrow
import random
from datetime import date
from . import db
from .token import Application
from .user import User, UserFriend


def add(*objects):
    for o in objects:
        db.session.add(o)


def reset_db():
    # Reset users
    admin = User(
        email='kokakiwi@kokakiwi.net', pseudo='kokakiwi', city='Seoul',
        birth_date=arrow.get('1992-08-10'), gender='male')
    admin.password = 'kiwi3291'
    florian = User(
        email='florian.faisan@epitech.eu', pseudo='kassisdion', city='Seoul',
        birth_date=arrow.get('1993-09-12'), gender='male')
    florian.password = 'florian'

    alice = User(
        email='alice@bob.com', pseudo='alice', city='CCrypto',
        birth_date=arrow.get('2010-10-10'), gender='female')
    alice.password = 'bob'

    add(admin, florian, alice)

    # Friends
    add(UserFriend(user=alice, friend=florian))
    add(UserFriend(user=admin, friend=alice))
    add(UserFriend(user=admin, friend=florian))

    # Reset apps
    app = Application(name='Test app', token='test')

    add(app)


def import_monsters():
    import requests
    from . import Monster, UserMonster

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
        monster.sprite = 'http://pokeapi.co/media/img/%d.png' % (obj['national_id'])

        db.session.add(monster)
        db.session.commit()
        monsters.append(monster)

    for user in User.query:
        select = random.sample(monsters, 5)
        for monster in select:
            user_monster = UserMonster(user=user, monster=monster)
            db.session.add(user_monster)

    db.session.commit()


def import_places():
    import requests
    from collections import namedtuple
    from geoalchemy2.shape import from_shape
    from shapely.geometry import Point
    from . import Monster, Place, Region, RegionMonster

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
    r = query_overpass('area["name:en"="Seoul"];out;node(area)[name];out 200 body;')
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

        # print('Importing %s...' % (point_name))
        point_place = Place(name=point_name, author=admin, point=point_data)
        db.session.add(point_place)

    monsters = Monster.query.all()
    for region in Region.query:
        select = random.sample(monsters, 10)
        for monster in select:
            region_monster = RegionMonster(region=region, monster=monster)
            region_monster.ratio = random.random()
            region_monster.level = [10, 60]
            db.session.add(region_monster)

    db.session.commit()
