
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

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'techisms', 
    }
}

WSGI_APPLICATION = 'techism.settings.staging_wsgi.application'

SESSION_COOKIE_SECURE = True
HTTPS_PATHS = (
    '/admin/',
    '/accounts/',
)
HTTP_URL = 'http://next.techism.de'
HTTPS_URL = 'https://next.techism.de'


### import settings stored in database

from database import *
