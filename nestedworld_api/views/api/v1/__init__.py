from ..utils import Api
from nestedworld_api.views.utils import NestableBlueprint as Blueprint

api_blueprint = Blueprint('v1', __name__)
api = Api(api_blueprint, title='NestedWorld API', version='1.0')


from . import user
