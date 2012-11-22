## import base settings

from base import *


## add or modify development specific settings

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
SECRET_KEY = 'dummy-for-development'
WSGI_APPLICATION = 'techism.settings.development_wsgi.application'
