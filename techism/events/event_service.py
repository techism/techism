#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import EventTag
from techism.models import Event

def get_tags():
    return EventTag.objects.all()

def __get_base_event_query_set():
    return Event.objects.filter(published__exact=True)

def get_upcomming_published_events_query_set():
    return __get_base_event_query_set().filter(archived__exact=False)

