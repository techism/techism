#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.core import serializers
import json
from django.utils import timezone
from techism.models import Event

'''[
    {
        "description": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut...", 
        "title": "Running event without end date", 
        "url": "http://example.com", 
        "canceled": false, 
        "date_time_end": "2013-04-28 17:04", 
        "date_time_begin": "2013-04-28 17:04", 
        "id": "5"
    }, 
    {
        ...
    }
   ]'''


def get_events_as_json(event_list):
    events = []
    for event in event_list:
        ev = dict()
        ev['id'] = str(event.id)
        ev['title'] = event.title
        date_time_begin_local = timezone.localtime(event.date_time_begin)
        date_time_begin_str = date_time_begin_local.strftime("%Y-%m-%d %H:%M")
        ev['date_time_begin'] = date_time_begin_str

        date_time_end_local = timezone.localtime(event.date_time_begin)
        date_time_end_str = date_time_end_local.strftime("%Y-%m-%d %H:%M")
        ev['date_time_end'] = date_time_end_str
        ev['url'] = event.url
        ev['description'] = event.description
        ev['canceled'] = event.canceled
        location = event.location
        if location:
            loc = dict()
            loc ['name'] = location.name
            loc ['street'] = location.street
            loc ['city'] = location.city
            loc ['latitude'] = location.latitude
            loc ['longitude'] = location.longitude
            ev['location'] = loc
        events.append(ev)
    events_as_json = json.dumps(events)
    return events_as_json

def get_event_from_json(json):
    #event_map = json.loads(json) @IndentOk
    #event = Event()
    #event.date_time_begin = event_map['date_time_end']
    #return event
    pass

def get_locations_as_json(location_list):
    locations = []
    for location in location_list:
        loc = dict()
        loc['id'] = location.id
        loc['name'] = location.name
        loc['street'] = location.street
        loc['city'] = location.city
        loc['latitude'] = location.latitude
        loc['longitude'] = location.longitude
        locations.append(loc)
    locations_as_json = json.dumps(locations)
    return locations_as_json
