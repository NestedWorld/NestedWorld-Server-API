from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .token import Application, Session
from .user import User
