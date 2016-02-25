from flask.ext.script import Manager
from ..app import app
from .db import db_manager

manager = Manager(app)
manager.add_command('db', db_manager)


@manager.command
def reset_password(email):
    '''Send a password reset request for an user'''
    from ..app import app
    from ..db import db
    from ..db import User, PasswordResetRequest
    from ..mail import TemplatedMessage

    user = User.query.filter(
        User.email == email, User.is_active is True).first()
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
