from pathlib import Path
from .secret import *

PROJECT_ROOT = Path().parent.resolve()

# Database config
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
