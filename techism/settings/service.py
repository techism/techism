#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import Setting

def get_secret_key():
    return get_setting('SECRET_KEY')

def get_twitter_consumer_key_for_login():
    return get_setting('TWITTER_CONSUMER_KEY_FOR_LOGIN')

def get_twitter_consumer_secret_for_login():
    return get_setting('TWITTER_CONSUMER_SECRET_FOR_LOGIN')

def get_twitter_consumer_key_for_tweets():
    return get_setting('TWITTER_CONSUMER_KEY_FOR_TWEETS')

def get_twitter_consumer_secret_for_tweets():
    return get_setting('TWITTER_CONSUMER_SECRET_FOR_TWEETS')

def get_twitter_access_key_for_shortterm_tweets():
    return get_setting('TWITTER_ACCESS_KEY_FOR_TWEETS')

def get_twitter_access_secret_for_shortterm_tweets():
    return get_setting('TWITTER_ACCESS_SECRET_FOR_TWEETS')

def get_twitter_access_key_for_longterm_tweets():
    return get_setting('TWITTER_ACCESS_KEY_FOR_LONGTERM_TWEETS')

def get_twitter_access_secret_for_longterm_tweets():
    return get_setting('TWITTER_ACCESS_SECRET_FOR_LONGTERM_TWEETS')

def get_setting(name):
    setting, _ = Setting.objects.get_or_create(name=name, defaults={'value': u'none'})
    value = setting.value
    return value



