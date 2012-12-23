#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from techism.events import event_service
from techism.models import TweetedEvent
from techism.settings import service
from techism import utils
from django.conf import settings
from django.utils import timezone
import tweepy
from tweepy.error import TweepError
import urllib
import logging
from datetime import timedelta

def tweet_upcoming_events():
    event_list = get_short_term_events()
    
    for event in event_list:
        must_tweet, prefix = __must_tweet_and_prefix(event)
        if must_tweet:
            tweet = format_tweet(event, prefix)
            try:
                __tweet_event(tweet)
                __mark_as_tweeted(event, tweet)
                break
            except TweepError, e:
                logger = logging.getLogger(__name__)
                logger.error(e.reason,  exc_info=True)
                if e.reason == u'Status is a duplicate.':
                    __mark_as_tweeted(event, tweet + " (duplicate)")
                    break
                else:
                    raise


def __must_tweet_and_prefix(event):
    # check if already tweeted, reweet only when changed
    tweet = None
    tweet_list = TweetedEvent.objects.filter(event=event).order_by('-date_time_created')
    if tweet_list:
        tweet = tweet_list[0]
        changed, prefix = utils.get_changed_and_change_prefix(event, tweet.date_time_created)
        if changed and not tweet.tweet.startswith(prefix):
            return (True, prefix)
        else:
            return (False, '')
    
    # always tweet canceled event once
    canceled, prefix = utils.get_canceled_and_cancel_prefix(event)
    if canceled:
        return (True, prefix)
    else:
        return (True, '')


def format_tweet(event, prefix):
    date_time_begin_localtime = timezone.localtime(event.date_time_begin)
    if event.get_number_of_days() > 0:
        date_time_end_localtime = timezone.localtime(event.date_time_end)
        date_string = date_time_begin_localtime.strftime("%d.%m.%Y") + "-" + date_time_end_localtime.strftime("%d.%m.%Y")
    else:
        date_string = date_time_begin_localtime.strftime("%d.%m.%Y %H:%M")
    
    base_url = settings.HTTP_URL
    relative_url = event.get_absolute_url()
    long_url = base_url + relative_url
    twitter_short_url_length = 25
    
    max_length = 140 - len(date_string) - twitter_short_url_length - len(prefix) - 5
    title = event.title[:max_length]
    
    tweet = u'%s%s - %s %s' % (prefix, title, date_string, long_url)
    
    return tweet


def get_short_term_events():
    now_utc = timezone.now()
    three_days = now_utc + timedelta(days=3)
    event_list = event_service.get_upcomming_published_events_query_set().filter(date_time_begin__gte=now_utc).filter (date_time_begin__lte=three_days).order_by('date_time_begin')
    return event_list


def __tweet_event(tweet):
    CONSUMER_KEY = service.get_twitter_consumer_key_for_tweets()
    CONSUMER_SECRET = service.get_twitter_consumer_secret_for_tweets()
    ACCESS_KEY = service.get_twitter_access_key_for_tweets()
    ACCESS_SECRET = service.get_twitter_access_secret_for_tweets()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(tweet)


def __mark_as_tweeted(event, tweet):
    tweeted_event = TweetedEvent()
    tweeted_event.event = event
    tweeted_event.tweet = tweet
    tweeted_event.save()
