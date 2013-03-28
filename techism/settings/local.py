
### import base settings

from base import *


### development specific settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('Test', 'test@example.com'),
)
MANAGERS = ADMINS
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'techism.sqlite', 
    }
}

WSGI_APPLICATION = 'techism.settings.local_wsgi.application'

SESSION_COOKIE_SECURE = False
HTTPS_PATHS = (
#    '/admin/',
#    '/accounts/',
)
HTTP_URL = 'http://localhost:8000'
HTTPS_URL = 'https://localhost:8443'

try:
    from debug_toolbar.middleware import DebugToolbarMiddleware
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.remove('techism.middleware.ContentSecurityPolicyMiddleware')
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS += ('debug_toolbar',)
except ImportError:
    pass

SECRET_KEY = 'dummy-for-development'

### import settings stored in database

from database import *
