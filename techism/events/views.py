#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from techism.events import event_service
from techism.models import Event

def index(request):
    event_list = event_service.get_upcomming_published_events_query_set
    tags = event_service.get_current_tags()
    return render_to_response('events/index.html', {'event_list': event_list}, context_instance=RequestContext(request))
