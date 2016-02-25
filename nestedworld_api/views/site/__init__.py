from .user import user
from ..utils import NestableBlueprint as Blueprint

site = Blueprint('site', __name__)
site.register_blueprint(user, url_prefix='/user')
