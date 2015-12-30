from flask import Flask

app = Flask(__name__)
app.config.from_object('nestedworld_api.settings')

# Config DB
from .db import db
db.init_app(app)

# Config Marshmallow
from flask.ext.marshmallow import Marshmallow
ma = Marshmallow(app)

# Config CORS
from flask.ext.cors import CORS
cors = CORS(app)

# Config mail
from .mail import mail
mail.init_app(app)

# Config mako
from flask.ext.mako import MakoTemplates
mako = MakoTemplates(app)

# Config debug toolbar
from flask.ext.debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

# Config logging
if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler

    handler = TimedRotatingFileHandler(str(app.config['LOG_FILE_PATH']))
    handler.setLevel(logging.WARNING)

    app.logger.addHandler(handler)

# Import views
from . import views
