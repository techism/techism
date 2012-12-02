
### import base settings

from base import *


### production specific settings

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'techismp', 
    }
}

WSGI_APPLICATION = 'techism.settings.production_wsgi.application'

SESSION_COOKIE_SECURE = True
HTTPS_PATHS = (
    '/admin/',
    '/accounts/',
)
HTTP_URL = 'http://next.techism.de:9080'
HTTPS_URL = 'https://next.techism.de:9443'


### import settings stored in database

from database import *
