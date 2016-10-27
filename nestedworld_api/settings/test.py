from .base import *

# Database config
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Debug Toolbar config
DEBUG_TB_ENABLED = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Mail config
MAIL_SERVER = 'mailtrap.io'
MAIL_PORT = 2525
MAIL_USERNAME = '463717942f08b4fca'
MAIL_PASSWORD = 'd87795288ee90a'
MAIL_DEFAULT_SENDER = 'noreply@nestedworld.io'

# Logging config
LOG_FILE_PATH = PROJECT_ROOT / 'logs' / 'api.log'
