#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.utils import timezone
from techism.events import event_service
from datetime import timedelta
from django.conf import settings
import urllib


def format_tweet(event, prefix):
    if event.takes_more_than_one_day():
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
