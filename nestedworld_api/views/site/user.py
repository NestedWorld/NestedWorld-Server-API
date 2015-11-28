from flask import abort, request
from flask.ext.mako import render_template
from flask.ext.wtf import Form
from nestedworld_api.views.utils import NestableBlueprint as Blueprint
from wtforms import PasswordField
from wtforms.validators import Required, EqualTo

user = Blueprint('user', __name__)

# Password reset

class PasswordReset(Form):

    password = PasswordField('Password', [Required(), EqualTo('confirm', message='Passwords must match')])
    confirm =  PasswordField('Repeat password')

@user.route('/password_reset/<token>', endpoint='password_reset', methods=['GET', 'POST'])
def password_reset(token):
    from nestedworld_api.db import db
    from nestedworld_api.db import PasswordResetRequest

    password_request = PasswordResetRequest.query\
                        .filter(PasswordResetRequest.token == token)\
                        .first()
    if password_request is None:
        abort(400, message='This password request token doesn\'t exists.')

    form = PasswordReset(request.form)
    if request.method == 'POST' and form.validate():
        user = password_request.user
        user.password = form.password.data

        PasswordResetRequest.query\
            .filter(PasswordResetRequest.user == user)\
            .delete()

        db.session.add(user)
        db.session.commit()

        return 'Your password has beed successfully set.'

    return render_template('user/password_reset.html', password_request=password_request, form=form)
