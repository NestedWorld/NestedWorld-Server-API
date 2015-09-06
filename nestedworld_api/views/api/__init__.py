from nestedworld_api.views.utils import NestableBlueprint as Blueprint
from .v1 import api_blueprint as api_v1

api = Blueprint('api', __name__)
api.register_blueprint(api_v1, url_prefix='/v1')
