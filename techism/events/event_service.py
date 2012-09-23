#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import EventTag
from techism.models import Event

def get_current_tags():
    return EventTag.objects.filter(event__archived = False, event__published=True)

def __get_base_event_query_set():
    return Event.objects.filter(published__exact=True)

def get_upcomming_published_events_query_set():
    return __get_base_event_query_set().filter(archived__exact=False)

