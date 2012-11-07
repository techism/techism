#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.template import Library 
from datetime import timedelta
from django.utils.translation import ugettext
from django.utils import timezone

register = Library()

@register.filter
def display_date(event_date):
    
    event_date_localtime = timezone.localtime(event_date)

    if not event_date_localtime:
        return '';
    elif (__is_today(event_date_localtime)):
        return u'Heute, ' + event_date_localtime.strftime("%H:%M")
    elif (__is_tomorrow(event_date_localtime)):
        return u'Morgen, ' + event_date_localtime.strftime("%H:%M")
    elif (__is_the_day_after_tomorrow(event_date_localtime)):
        return u'Übermorgen, ' + event_date_localtime.strftime("%H:%M")
    else:
        weekday = ugettext (event_date_localtime.strftime("%A"))[:2]
        day = event_date_localtime.day
        month = ugettext (event_date_localtime.strftime("%B"))[:3]
        time = event_date_localtime.strftime("%H:%M")
        return weekday + ", " + str(day) + ". " + month + " " + time


def __is_today(event_date_localtime):
    return event_date_localtime.date() == __today_localtime()

def __is_tomorrow(event_date_localtime):
    return event_date_localtime.date() == __today_localtime() + timedelta(days=1)

def __is_the_day_after_tomorrow(event_date_localtime):
    return event_date_localtime.date() == __today_localtime() + timedelta(days=2)

def __today_localtime():
    return timezone.localtime(timezone.now()).date()
