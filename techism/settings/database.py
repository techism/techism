
### settings in database

from django.db.utils import DatabaseError
from techism.settings import service as settings_service

try:
    SECRET_KEY = settings_service.get_secret_key()
    TWITTER_CONSUMER_KEY = settings_service.get_twitter_consumer_key_for_login()
    TWITTER_CONSUMER_SECRET = settings_service.get_twitter_consumer_secret_for_login()
except DatabaseError:
    from django.db import connection
    connection._rollback()


### additional permissions

from django.db.models.signals import post_syncdb
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from techism.models import Event

def add_custom_permissions(sender, **kwargs):
    ct = ContentType.objects.get_for_model(model=Event)
    Permission.objects.get_or_create(codename='use_api', name='Use API', content_type=ct)
post_syncdb.connect(add_custom_permissions)