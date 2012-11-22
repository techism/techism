## import base settings

from base import *


## add or modify development specific settings

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
SECRET_KEY = open(os.path.expanduser('~/.techismp.secret')).read().strip()
WSGI_APPLICATION = 'techism.settings.production_wsgi.application'
