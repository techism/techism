#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import Setting

def get_secret_key():
    return get_setting('SECRET_KEY')

def get_twitter_consumer_key_for_login():
    return get_setting('TWITTER_CONSUMER_KEY_FOR_LOGIN')

def get_twitter_consumer_secret_for_login():
    return get_setting('TWITTER_CONSUMER_SECRET_FOR_LOGIN')

def get_setting(name):
    setting, _ = Setting.objects.get_or_create(name=name, defaults={'value': u'none'})
    value = setting.value
    return value



