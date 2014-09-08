#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pytz
from pytz import timezone as pytz_timezone
from datetime import datetime
from django.core import serializers
import json
from django.utils import timezone
from techism.models import Event
from techism.events.forms import convert_to_event_tags

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


def __date_time_to_json_string(date_time):
    date_time_local = timezone.localtime(date_time)
    date_time_str = date_time_local.strftime("%Y-%m-%d %H:%M")
    return date_time_str

def __json_string_to_date_time(date_time_str):
    date_time_native = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
    cet = pytz_timezone('Europe/Berlin')
    date_time_local = cet.localize(date_time_native)
    date_time_utc = date_time_local.astimezone(pytz.utc)
    return date_time_utc

def get_events_as_json(event_list):
    events = []
    for event in event_list:
        ev = dict()
        ev['id'] = str(event.id)
        ev['title'] = event.title
        ev['date_time_begin'] = __date_time_to_json_string(event.date_time_begin)
        if event.date_time_end:
            ev['date_time_end'] = __date_time_to_json_string(event.date_time_end)
        ev['url'] = event.url
        ev['description'] = event.description
        ev['canceled'] = event.canceled
        ev['tags'] = [tag.name.encode('utf-8') for tag in event.tags.all()]
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

def save_event_from_json(event_as_json, user):
    ev = json.loads(event_as_json)
    
    event = Event()
    event.user = user
    if 'id' in ev:
        event.id = ev['id']
    
    event.title = ev['title']
    
    if 'date_time_begin' in ev:
        event.date_time_begin = __json_string_to_date_time(ev['date_time_begin'])
    if 'date_time_end' in ev:
        event.date_time_end = __json_string_to_date_time(ev['date_time_end'])

    if 'url' in ev:
        event.url = ev['url']
    if 'description' in ev:
        event.description = ev['description']
    if 'canceled' in ev:
        event.canceled = ev['canceled']

    event.save()

    if 'tags' in ev:
        tags = convert_to_event_tags(ev['tags'])
        event.tags = tags
        event.save()

    # TODO: location
    
    return event

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
