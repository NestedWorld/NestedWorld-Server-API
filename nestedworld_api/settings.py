import os
from pathlib import Path
from .secret import *

PROJECT_ROOT = Path().parent.resolve()

# Database config
if 'DATABASE_URL' in os.environ:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
else:
    DB_PATH = PROJECT_ROOT / 'db.sqlite3'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (DB_PATH)

SQLALCHEMY_ECHO = True

# Passwords config
PASSWORD_SCHEMES = [
    'pbkdf2_sha512',
]

# Templates config
MAKO_TRANSLATE_EXCEPTIONS = False

# Debug toolbar config
DEBUG_TB_ENABLED = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Auth config
RBAC_USE_WHITE = False

# Mail config
MAIL_SERVER = 'mailtrap.io'
MAIL_PORT = 2525
MAIL_USERNAME = '463717942f08b4fca'
MAIL_PASSWORD = 'd87795288ee90a'
MAIL_DEFAULT_SENDER = 'noreply@nestedworld.io'
