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
        birth_date=arrow.get('1992-08-10').datetime.date(), gender='male')
    admin.password = 'kiwi3291'

    florian = User(
        email='florian.faisan@epitech.eu', pseudo='kassisdion', city='Seoul',
        birth_date=arrow.get('1993-09-12').datetime.date(), gender='male')
    florian.password = 'florian'

    alice = User(
        email='alice@bob.com', pseudo='alice', city='CCrypto',
        birth_date=arrow.get('2010-10-10').datetime.date(), gender='female')
    alice.password = 'bob'

    thomas = User(
        email='thomas.caron@epitech.eu', pseudo='barbu', city='Lille',
        birth_date=arrow.get('1994-07-06').datetime.date(), gender='male')
    thomas.password = 'mexico'

    add(admin, florian, alice, thomas)

    # Friends
    add(UserFriend(user=alice, friend=florian))
    add(UserFriend(user=admin, friend=alice))
    add(UserFriend(user=admin, friend=florian))
    add(UserFriend(user=thomas, friend=florian))
    add(UserFriend(user=thomas, friend=alice))

    # Reset apps
    app = Application(name='Test app', token='test')

    add(app)


def import_monsters():
    import json
    from . import Monster, UserMonster

    print('Fetching data...')
    data = json.load(open('monsters.json'))
    objects = data['objects']

    print('Importing data...')
    monsters = []
    for obj in objects:
        monster = Monster()
        monster.name = obj['name']
        monster.hp = obj['hp']
        monster.attack = obj['attack']
        monster.defense = obj['defense']
        monster.speed = obj['speed']
        if obj['types'][0]['name'] == 'electric':
            monster.type = 'electric'
        elif obj['types'][0]['name'] == 'grass':
            monster.type = 'plant'
        elif obj['types'][0]['name'] == 'rock' or obj['types'][0]['name'] == 'ground':
            monster.type = 'earth'
        elif obj['types'][0]['name'] == 'fire':
            monster.type = 'fire'
        elif obj['types'][0]['name'] == 'water':
            monster.type = 'water'
        else :
            monster.type = 'plant'

        monster.base_sprite = 'https://s3-eu-west-1.amazonaws.com/nestedworld/Monsters/default_monster.png'
        monster.enraged_sprite = 'https://s3-eu-west-1.amazonaws.com/nestedworld/Monsters/default_monster.png'

        db.session.add(monster)
        db.session.commit()
        monsters.append(monster)

    for user in User.query:
        select = random.sample(monsters, 5)
        for monster in select:
            user_monster = UserMonster(user=user, monster=monster, \
            level=0, experience=0, surname="IAMTOTORO")
            db.session.add(user_monster)

    db.session.commit()

def import_attacks():
    import json
    from . import Monster, Attack, MonsterAttack

    data = json.load(open('attacks.json'))
    objects = data['objects']

    print('Importing data...')
    attacks = []
    for obj in objects:
        attack = Attack()
        attack.name = obj['name']
        if obj['id'] % 4 == 0:
            attack.type = 'attack'
        elif obj['id'] % 3 == 0:
            attack.type = 'defense'
        elif obj['id'] % 2 == 0:
            attack.type = 'defensesp'
        else:
            attack.type = 'attacksp'

        db.session.add(attack)
        db.session.commit()
        attacks.append(attack)

    for monster in Monster.query:
        select = random.sample({attack for attack in attacks if attack.type == 'attack'}, 1)
        select += random.sample({attack for attack in attacks if attack.type == 'attacksp'}, 1)
        select += random.sample({attack for attack in attacks if attack.type == 'defense'}, 1)
        select += random.sample({attack for attack in attacks if attack.type == 'defensesp'}, 1)

        for attack in select:
            monster_attack = MonsterAttack(attack=attack, monster=monster)
            db.session.add(monster_attack)

    db.session.commit()

def import_portals():
    import requests
    from collections import namedtuple
    from geoalchemy2.shape import from_shape
    from shapely.geometry import Point
    from . import Monster, Portal, Region, RegionMonster, PortalMonster

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
    r = query_overpass('area(3600058404)->.searchArea;(node["amenity"](area.searchArea););out body;')
    points = r[0:]

    # City
    city_rel_id = int(3600058404 - 3.6e9)
    city_polygon = get_polygon(city_rel_id)

    city_name = "Lille"

    print('Importing %s...' % (city_name))
    city_region = Region(name=city_name, zone=city_polygon)
    db.session.add(city_region)

    # Points
    for point in points:
        point_data = from_shape(Point(point['lon'], point['lat']))

        point_tags = point['tags']
        point_name = point_tags.get('name:en', point_tags.get('name'))

        type = ['water', 'fire', 'earth', 'electric', 'plant']
        if point_name is not None :
        # print('Importing %s...' % (point_name))
            point_portal = Portal(name=point_name, author=admin, point=point_data, type=random.sample(type, 1)[0])
            db.session.add(point_portal)

    monsters = Monster.query.all()
    for region in Region.query:
        select = random.sample(monsters, 10)
        for monster in select:
            region_monster = RegionMonster(region=region, monster=monster)
            region_monster.ratio = random.random()
            region_monster.level = [10, 60]
            db.session.add(region_monster)

    for portal in Portal.query:
        select = random.sample(monsters, 4)
        for monster in select:
            portal_monster = PortalMonster(portal=portal, monster=monster)
            db.session.add(portal_monster)

    db.session.commit()

def import_objects():

    from . import Plant
    from . import Inventory

    plants = []
    fire = Plant(
        name='fire flower', description='a fire flower. Use it for up your attacksp.', premium=False,
        price=25, image='http://www.mariowiki.com/images/thumb/6/6a/FireFlowerMK8.png/200px-FireFlowerMK8.png', type='plant', kind="attsp-up", power="1")

    water = Plant(
        name='water flower', description='a water flower. Use it for up your defensesp.', premium=True,
        price=25, image='https://s3-eu-west-1.amazonaws.com/nestedworld/Items/flowerFire.png', type='plant', kind="defsp-up", power="1")

    electric = Plant(
        name='electric flower', description='a electric flower. Use it for for up your attack.', premium=True,
        price=25, image='https://s3-eu-west-1.amazonaws.com/nestedworld/Items/flowerElec.png', type='plant', kind="att-up", power="1")

    grass = Plant(
        name='grass flower', description='a grass flower. Use it for for up your defense.', premium=True,
        price=25, image='https://s3-eu-west-1.amazonaws.com/nestedworld/Items/flowerGrass.png', type='plant', kind="def-up", power="1")

    dirt = Plant(
        name='dirt flower', description='a dirt flower. Use it for up your defense.', premium=True,
        price=25, image='https://s3-eu-west-1.amazonaws.com/nestedworld/Items/flowerDirt.png', type='plant', kind="def-up", power="1")


    flower = Plant(
        name='flower', description='a simple flower. Use it for healing monster.', premium=True,
        price=25, image='https://s3-eu-west-1.amazonaws.com/nestedworld/Items/Flower.png', type='plant', kind="heal", power="50")


    plants.append(fire)
    plants.append(water)
    plants.append(dirt)
    plants.append(electric)
    plants.append(grass)
    plants.append(flower)
    add(fire, water, dirt, electric, grass, flower)
    db.session.commit()

    for user in User.query:
        select = random.sample(plants, 5)
        for plant in select:
            object = Inventory(user=user, object=plant)
            db.session.add(object)
    db.session.commit()
