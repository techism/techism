
### settings in database

from django.db.utils import DatabaseError
from techism.settings import service as settings_service

try:
    SECRET_KEY = settings_service.get_secret_key()
    TWITTER_CONSUMER_KEY = settings_service.get_twitter_consumer_key_for_login()
    TWITTER_CONSUMER_SECRET = settings_service.get_twitter_consumer_secret_for_login()
    TWITTER_ACCESS_KEY = settings_service.get_twitter_access_key_for_tweets()
    TWITTER_ACCESS_SECRET = settings_service.get_twitter_access_secret_for_tweets()
except DatabaseError:
    from django.db import connection
    connection._rollback()
