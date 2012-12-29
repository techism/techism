
### import base settings

from base import *


### prod specific settings

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('Techism Team', 'team@techism.de'),
)
MANAGERS = ADMINS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[Techism] '

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'techismp', 
    }
}

WSGI_APPLICATION = 'techism.settings.prod_wsgi.application'

SESSION_COOKIE_SECURE = True
HTTPS_PATHS = (
    '/admin/',
    '/accounts/',
)
HTTP_URL = 'http://www.techism.de'
HTTPS_URL = 'https://www.techism.de'

LOGGING['handlers']['errorlogfile']['filename'] = '/srv/www/techism-prod-log/error.log'
LOGGING['handlers']['debuglogfile']['filename'] = '/srv/www/techism-prod-log/debug.log'


### import settings stored in database

from database import *
