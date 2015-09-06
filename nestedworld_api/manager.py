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
    from .settings import DB_PATH

    # Remove old DB
    if DB_PATH.exists():
        DB_PATH.unlink()

    db.create_all()
    fixtures.reset_db()
    db.session.commit()
