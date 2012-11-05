#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from techism.events import event_service
from techism.ical import ical_service
from techism.models import Event
from datetime import datetime, timedelta


def ical(request):
    ninety_days = datetime.utcnow() + timedelta(days=90)
    event_list = event_service.get_upcomming_published_events_query_set().filter(date_time_begin__lte=ninety_days).order_by('date_time_begin')
    cal = ical_service.create_calendar_with_metadata(event_list, request)
    response = create_httpresponse(cal.as_string())
    return response


def ical_single_event (request, event_id):
    e = get_object_or_404(Event, id=event_id)
    event_list = [e]
    cal = ical_service.create_calendar_with_metadata(event_list, request)
    response = create_httpresponse(cal.as_string())
    return response


def create_httpresponse (content):
    response = HttpResponse(content)
    response['Content-Type'] = 'text/calendar; charset=UTF-8'
    response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'
    return response


