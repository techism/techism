
### import base settings

from base import *


### env specific settings

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

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'techism', 
    }
}

WSGI_APPLICATION = 'techism.settings.techism_wsgi.application'

SESSION_COOKIE_SECURE = True
HTTPS_PATHS = (
    '/admin/',
    '/accounts/',
)
ALLOWED_HOSTS = ['www.techism.de']
HTTP_URL = 'http://www.techism.de'
HTTPS_URL = 'https://www.techism.de'

LOGGING['handlers']['errorlogfile']['filename'] = '/var/log/techism/error.log'
LOGGING['handlers']['debuglogfile']['filename'] = '/var/log/techism//debug.log'


### import settings stored in database

from database import *
