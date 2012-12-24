import os.path

TIME_ZONE = 'Europe/Berlin'

LANGUAGE_CODE = 'de-DE'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

SERVER_EMAIL = 'webmaster@techism.de'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static-collected'))

# URL prefix for static files.
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../static')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (  
    'django.template.loaders.filesystem.Loader',  
    'django.template.loaders.app_directories.Loader',  
)  

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'techism.middleware.SecureRequiredMiddleware',
    'techism.middleware.ContentSecurityPolicyMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'techism.urls'

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'techism',
    'techism.events',
    'techism.organizations',
    'techism.ical',
    'techism.rss',
    'techism.twitter',
    'django.contrib.admin',
    'social_auth',
    'reversion',
    'south'
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.OpenIDBackend',
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/accounts/logout/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : '[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)s] %(message)s',
        },
    },
    'handlers': {
        'errorlogfile': {
            'level':'WARNING',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': 'log/error.log',
            'when': 'midnight',
            'utc' : True,
            'backupCount': 30,
            'formatter': 'standard',
        },
        'debuglogfile': {
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': 'log/debug.log',
            'when': 'midnight',
            'utc' : True,
            'backupCount': 30,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['errorlogfile', 'debuglogfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'techism': {
        'handlers': ['errorlogfile', 'debuglogfile'],
        'level': 'DEBUG',
        'propagate': False,
        },
    }
}
