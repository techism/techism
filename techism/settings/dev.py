
### import base settings

from base import *


### staging specific settings

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('Christine Koppelt', 'ch.ko123@gmail.com'),
    ('Stefan Seelmann', 'stefseel@gmail.com'),
)
MANAGERS = ADMINS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[Techism Development] '

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'techismd', 
    }
}

WSGI_APPLICATION = 'techism.settings.dev_wsgi.application'

SESSION_COOKIE_SECURE = True
HTTPS_PATHS = (
    '/admin/',
    '/accounts/',
)
ALLOWED_HOSTS = ['dev.techism.de']
HTTP_URL = 'http://dev.techism.de'
HTTPS_URL = 'https://dev.techism.de'

LOGGING['handlers']['errorlogfile']['filename'] = '/srv/www/techism-dev-log/error.log'
LOGGING['handlers']['debuglogfile']['filename'] = '/srv/www/techism-dev-log/debug.log'


### import settings stored in database

from database import *
