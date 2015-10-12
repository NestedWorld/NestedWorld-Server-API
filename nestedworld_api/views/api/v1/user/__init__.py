from flask.ext.restplus import Resource, fields
from nestedworld_api.login import login_required, current_session
from .. import api

user = api.namespace('users', description='User operations')


from . import auth


@user.route('/')
class User(Resource):

    __apidoc__ = {
        'params': auth.AUTH_REQUIRED_PARAMS,
    }

    parser = user.parser()
    parser.add_argument(
        'email', type=str, required=False, help='User email', location='form')
    parser.add_argument(
        'pseudo', type=str, required=False, help='User pseudonyme', location='form')
    parser.add_argument(
        'birth_date', type=str, required=False, help='User birth date', location='form')
    parser.add_argument(
        'city', type=str, required=False, help='User city', location='form')
    parser.add_argument(
        'gender', type=str, required=False, help='User gender', location='form')

    result = user.model('UserResult', {
        'email': fields.String(required=True, description='User email'),
        'pseudo': fields.String(required=True, description='User pseudo'),
        'birth_date': fields.String(required=True, description='User birth date'),
        'city': fields.String(required=True, description='User city'),
        'gender': fields.String(required=True, description='User gender'),
    })

    @login_required
    def get(self):
        import json

        data = {}

        data['email'] = current_session.user.email
        data['registered_at'] = str(current_session.user.registered_at)
        data['is_active'] = current_session.user.is_active
        data['pseudo'] = current_session.user.pseudo
        data['birth_date'] = str(current_session.user.birth_date)
        data['city'] = current_session.user.city
        data['gender'] = current_session.user.gender
        json_data = json.dumps(data)
        return json_data

    @user.doc(parser=parser)
    @user.marshal_with(result)
    @login_required
    def put(self):
        from nestedworld_api.db import db
        from nestedworld_api.db import Application, User as DbUser
        import arrow

        args = User.parser.parse_args()

        if args.gender != 'female' and args.gender != 'male' and args.gender != 'other':
            user.abort(400, 'User gender is incorrect')
        try:
            arrow.get(args.birth_date)
        except:
            user.abort(400, 'Date is incorrect')

        if args.email is not None :
            current_session.user.email = args.email
        if args.pseudo is not None :
            current_session.user.pseudo = args.pseudo
        if args.birth_date is not None :
            current_session.user.birth_date = arrow.get(args.birth_date)
        if args.city is not None :
            current_session.user.city = args.city
        if args.gender is not None :
            current_session.user.gender = args.gender

        db.session.commit()

        return current_session.user