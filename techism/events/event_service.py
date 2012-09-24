#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import EventTag
from techism.models import Event
from django.db.models import Count

def get_current_tags():
    return EventTag.objects.filter(event__archived = False, event__published=True).annotate(num_tags=Count('name')).order_by('name').iterator()

def __get_base_event_query_set():
    return Event.objects.filter(published__exact=True)

def get_upcomming_published_events_query_set():
    return __get_base_event_query_set().filter(archived__exact=False)

