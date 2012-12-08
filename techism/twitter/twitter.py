#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.utils import timezone
from techism.events import event_service
from techism.models import TweetedEvent
from datetime import timedelta
from django.conf import settings
import urllib

def tweet_upcoming_events():
    event_list = get_short_term_events()
    
    for event in event_list:
        must_tweet, prefix = __must_tweet_and_prefix(event)
        if must_tweet:
            tweet = format_tweet(event, prefix)
            #todo
            print tweet
    raise Exception ("not implemented yet")


def __must_tweet_and_prefix(event):
    # get last tweet
    tweet = None
    tweet_list = TweetedEvent.objects.filter(event=event).order_by('-date_time_created')
    if tweet_list.exists():
        tweet = tweet_list[0]
    
    # determine if we must tweet and the used prefix
    if event.canceled:
        if tweet is None or not tweet.tweet.startswith('[Abgesagt] '):
            return (True, '[Abgesagt] ')
    else:
        if tweet is None:
            return (True, '')
        elif not tweet.tweet.startswith('[Update] '):
            cl_list = EventChangeLog.objects.filter(event=event).filter(date_time__gte=tweet.date_time_created).order_by('-date_time')
            if cl_list.exists():
                return (True, '[Update] ')
    
    return (False, '')


def format_tweet(event, prefix):
    if event.get_number_of_days() > 0:
        date_string = event.date_time_begin.strftime("%d.%m.%Y") + "-" + event.date_time_end.strftime("%d.%m.%Y")
    else:
        date_string = event.date_time_begin.strftime("%d.%m.%Y %H:%M")
    
    base_url = settings.HTTP_URL
    relative_url = event.get_absolute_url()
    long_url = base_url + relative_url
    twitter_short_url_length = 25
    
    max_length = 140 - len(date_string) - twitter_short_url_length - len(prefix) - 5
    title = event.title[:max_length]
    
    tweet = u'%s%s - %s %s' % (prefix, title, date_string, long_url)
    
    return tweet


def get_short_term_events():
    today_local = timezone.localtime(timezone.now())
    three_days = today_local + timedelta(days=3)
    event_list = event_service.get_upcomming_published_events_query_set().filter(date_time_begin__gte=today_local).filter (date_time_begin__lte=three_days).order_by('date_time_begin')
    return event_list
