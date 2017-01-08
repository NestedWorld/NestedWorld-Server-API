from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from ..app import app
from ..db import db, fixtures

migrate = Migrate(app, db)


# Management
db_manager = Manager(help='Database management commands', description='')
db_manager.add_command('migrate', MigrateCommand)


@db_manager.command
def reset():
    '''Reset the database'''

    db.drop_all()
    db.create_all()
    fixtures.reset_db()
    db.session.commit()


@db_manager.command
def import_monsters():
    fixtures.import_monsters()


@db_manager.command
def import_portals():
    fixtures.import_portals()


@db_manager.command
def import_attacks():
    fixtures.import_attacks()


@db_manager.command
def import_objects():
    fixtures.import_objects()


@db_manager.command
def full_reset():
    db.drop_all()
    db.create_all()
    fixtures.reset_db()
    db.session.commit()
    fixtures.import_monsters()
    fixtures.import_attacks()
    fixtures.import_portals()
    fixtures.import_objects()
