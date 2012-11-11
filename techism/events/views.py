#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from techism.events import event_service
from techism.events.forms import EventForm
from techism.models import Event, EventTag

def index(request):
    event_list = event_service.get_upcomming_published_events_query_set
    tags = event_service.get_current_tags()
    return render_to_response(
        'events/index.html',
        {
            'event_list': event_list,
            'tags': tags,
            'hostname': request.get_host()
        },
        context_instance=RequestContext(request))

def details(request, event_id):
    # the event_id may be the slugified, e.g. 'munichjs-meetup-286002'
    splitted_event_id = event_id.rsplit('-', 1)
    if len(splitted_event_id) > 1:
        event_id = splitted_event_id[1]
    
    tags = event_service.get_current_tags()
    event = get_object_or_404(Event, id=event_id)
    return render_to_response(
        'events/details.html',
        {
            'event': event,
            'tags': tags,
            'hostname': request.get_host()
        },
        context_instance=RequestContext(request))

def tag(request, tag_name):
    tag = get_object_or_404(EventTag, name=tag_name)
    event_list = event_service.get_upcomming_published_events_query_set().filter(tags=tag).order_by('date_time_begin')
    tags = event_service.get_current_tags()
    return render_to_response(
        'events/index.html', 
        {
            'event_list': event_list, 
            'tags': tags, 
            'tag_name': tag_name
        }, 
        context_instance=RequestContext(request))

def create(request, event_id=None):
    button_label = u'Event hinzuf\u00FCgen'
    
    form = EventForm()
    
    return render_to_response(
        'events/create.html',
        {
            'form': form,
            'button_label': button_label
        },
        context_instance=RequestContext(request))
