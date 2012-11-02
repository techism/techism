#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from techism.events import event_service
from techism.models import Event

def index(request):
    event_list = event_service.get_upcomming_published_events_query_set
    tags = event_service.get_current_tags()
    return render_to_response(
        'events/index.html',
        {
            'event_list': event_list,
            'tags': tags
        },
        context_instance=RequestContext(request))

def details(request, event_id):
    # the event_id may be the slugified, e.g. 'munichjs-meetup-286002'
    splitted_event_id = event_id.rsplit('-', 1)
    if len(splitted_event_id) > 1:
        event_id = splitted_event_id[1]
    
    tags = event_service.get_current_tags()
    event = Event.objects.get(id=event_id)
    return render_to_response(
        'events/details.html',
        {
            'event': event,
            'tags': tags
        },
        context_instance=RequestContext(request))
