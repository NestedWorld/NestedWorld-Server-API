from flask import Flask

app = Flask(__name__)
app.config.from_object('nestedworld_api.settings')

# Config DB
from .db import db
db.init_app(app)

# Import views
from . import views
