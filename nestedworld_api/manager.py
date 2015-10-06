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
