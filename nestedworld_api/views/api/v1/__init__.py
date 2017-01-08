from apispec import APISpec
from flask_guimauve import Api
from nestedworld_api.views.utils import NestableBlueprint as Blueprint

api_blueprint = Blueprint('v1', __name__)

spec = APISpec(
    title='Nestedworld API',
    version='0.1.0',
    basePath='/v1',
)

api = Api(spec, api_blueprint)


from . import geo, monster, user, attack, object, exchange
