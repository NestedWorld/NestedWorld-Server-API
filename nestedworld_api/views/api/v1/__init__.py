from flask.ext.guimauve import Api
from nestedworld_api.views.utils import NestableBlueprint as Blueprint

api_blueprint = Blueprint('v1', __name__)
api = Api(None, api_blueprint)


from . import monster, user
