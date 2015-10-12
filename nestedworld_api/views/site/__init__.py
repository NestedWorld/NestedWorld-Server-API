from nestedworld_api.views.utils import NestableBlueprint as Blueprint
from .user import user

site = Blueprint('site', __name__)
site.register_blueprint(user, url_prefix='/user')
