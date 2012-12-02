
### import base settings

from base import *


### development specific settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'techism.sqlite', 
    }
}

WSGI_APPLICATION = 'techism.settings.development_wsgi.application'

SESSION_COOKIE_SECURE = False
HTTPS_PATHS = (
#    '/admin/',
#    '/accounts/',
)
HTTP_URL = 'http://localhost:8000'
HTTPS_URL = 'https://localhost:8443'


### import settings stored in database

from database import *
