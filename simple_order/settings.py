import importlib.util
import locale
import os
import sys
from pathlib import Path

os.environ['LANG'] = 'C.UTF-8'
os.environ['LC_ALL'] = 'C.UTF-8'
locale.setlocale(locale.LC_ALL, 'C.UTF-8')

if '' in sys.path:
    sys.path.remove('')
if '.' in sys.path:
    sys.path.remove('.')

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

DATA_DIR = Path('/opt/simple-order/data')
DATA_DIR.mkdir(parents=True, exist_ok=True)
PRIVATE_DIR = DATA_DIR / 'private'
PRIVATE_DIR.mkdir(exist_ok=True)
TMP_DIR = DATA_DIR / 'tmp'
TMP_DIR.mkdir(exist_ok=True)

FILE_UPLOAD_TEMP_DIR = TMP_DIR
FILE_UPLOAD_PERMISSIONS = 0o644

DEBUG = False
DEBUG_TOOLBAR = False

ADMINS = (
    ('Admin', 'admin@server.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PRIVATE_DIR / 'db.sqlite3',
    }
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ALLOWED_HOSTS = ['*']
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr'

LANGUAGES = (
    ('en', 'English'),
    ('fr', 'Français'),
)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False
USE_L10N = False

# Dates format
DATE_FORMAT = 'Y-m-d'
DATE_INPUT_FORMATS = ['%Y-%m-%d']

# Absolute path to the directory that holds media.
# Example: '/home/media/media.lawrence.com/'
MEDIA_ROOT = DATA_DIR / 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: 'http://media.lawrence.com', 'http://example.com/media/'
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATIC_DIR = Path('/opt/simple-order/repo/deployment/static')  # this var is not used by Django
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    STATIC_DIR,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'should be overwritten in local settings'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                # 'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                # 'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'simple_order.base.context_processors.common',
            )
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'simple_order.urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'simple_order.base',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'django.contrib.auth.backends.RemoteUserBackend',
)

# Logging config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '%(asctime)s %(module)s %(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'django_log_file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': str(TMP_DIR / 'django.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['django_log_file'],
        'level': 'INFO',
        'propagate': False,
    },
}

# Session config
SESSION_COOKIE_NAME = 'sosessionid'
SESSION_COOKIE_AGE = 6 * 3600  # in seconds
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_AGE = None

# Auth config
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Email config
SERVER_EMAIL = 'server@host.com'  # Used as sender for error emails
DEFAULT_FROM_EMAIL = 'server@host.com'   # Used as sender for other emails
EMAIL_USE_TLS = False
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25

# Simple order
SO_SITE_TITLE = 'Site title'
SO_OWNER_NAME = 'Test Owner'
SO_OWNER_ADDRESS = '98 Wild street\n12345 Here'

# Import local settings
# ---------------------
OVERRIDE_PATH = PRIVATE_DIR / 'settings_override.py'
if OVERRIDE_PATH.exists():
    spec = importlib.util.spec_from_file_location('settings_override', OVERRIDE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules['settings_override'] = mod
    from settings_override import *  # NOQA: F401,F403

# Apply changes depending on local settings
# -----------------------------------------
SERVER_EMAIL = DEFAULT_FROM_EMAIL

if DEBUG_TOOLBAR:
    DEBUG = True
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    if 'INTERNAL_IPS' not in globals():
        INTERNAL_IPS = '127.0.0.1'
elif os.environ.get('DEBUG'):
    DEBUG = os.environ['DEBUG'] == 'on'
if DEBUG:
    TEMPLATES[0]['OPTIONS']['debug'] = True
    TEMPLATES[0]['OPTIONS']['string_if_invalid'] = 'Invalid template string: "%s"'
    LOGGING['root']['level'] = 'DEBUG'
    LOGGING['root']['handlers'] = ['console']
    del LOGGING['loggers']['django.request']['handlers']
    import warnings
    warnings.simplefilter('always')
    warnings.simplefilter('ignore', ResourceWarning)  # Hide unclosed files warnings
    os.environ['PYTHONWARNINGS'] = 'always'  # Also affect subprocesses
else:
    import logging
    logging.captureWarnings(False)

# Disable logging config for daemons
if os.environ.get('DJANGO_LOGGING') == 'none':
    LOGGING_CONFIG = None
