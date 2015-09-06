from flask.ext.restplus import apidoc
from nestedworld_api.app import app
from .api import api

app.register_blueprint(api)
app.register_blueprint(apidoc.apidoc)
