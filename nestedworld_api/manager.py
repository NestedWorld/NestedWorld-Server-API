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
    from . import settings

    # Remove old DB
    if hasattr(settings, 'DB_PATH'):
        DB_PATH = settings.DB_PATH
        if DB_PATH.exists():
            DB_PATH.unlink()

    db.drop_all()
    db.create_all()
    fixtures.reset_db()
    db.session.commit()
