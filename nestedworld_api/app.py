import os
from flask import Flask

app = Flask(__name__)
app.config.from_object(os.environ.get('NESTEDWORLD_API_SETTINGS', 'nestedworld_api.settings.dev'))

# Config DB
from .db import db
db.init_app(app)

# Config Marshmallow
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

# Config CORS
from flask_cors import CORS
cors = CORS(app)

# Config mail
from .mail import mail
mail.init_app(app)

# Config mako
from flask_mako import MakoTemplates
mako = MakoTemplates(app)

# Config debug toolbar
# from flask_debugtoolbar import DebugToolbarExtension
# toolbar = DebugToolbarExtension(app)

# Config logging
if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler

    handler = TimedRotatingFileHandler(str(app.config['LOG_FILE_PATH']))
    handler.setLevel(logging.WARNING)

    app.logger.addHandler(handler)

# Import views
from . import views
