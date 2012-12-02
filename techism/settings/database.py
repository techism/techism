
### settings in database

from techism.settings import service as settings_service

SECRET_KEY = settings_service.get_secret_key()

TWITTER_CONSUMER_KEY = settings_service.get_twitter_consumer_key_for_login()
TWITTER_CONSUMER_SECRET = settings_service.get_twitter_consumer_secret_for_login()

