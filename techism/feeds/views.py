#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from techism.events import event_service
from techism.models import Event
from datetime import datetime, timedelta
import icalendar
import time


def ical(request):
    ninety_days = datetime.utcnow() + timedelta(days=90)
    event_list = event_service.get_upcomming_published_events_query_set().filter(date_time_begin__lte=ninety_days).order_by('date_time_begin')
    cal = create_calendar_with_metadata()
    for e in event_list:
        event = create_ical_entry(e, request)
        cal.add_component(event)
    response = create_httpresponse(cal.to_ical())
    return response


def ical_single_event (request, event_id):
    e = Event.objects.get(id=event_id)
    cal = create_calendar_with_metadata()
    event = create_ical_entry(e, request)
    cal.add_component(event)
    response = create_httpresponse(cal.to_ical())
    return response


def create_calendar_with_metadata ():
    cal = icalendar.Calendar()
    cal['prodid'] = icalendar.vText(u'-//Techism//Techism//DE')
    cal['version'] = icalendar.vText(u'2.0')
    cal['x-wr-calname'] = icalendar.vText(u'Techism')
    cal['x-wr-caldesc'] = icalendar.vText(u'Techism - Events, Projekte, User Groups in München')
    return cal

def create_httpresponse (content):
    response = HttpResponse(content)
    response['Content-Type'] = 'text/calendar; charset=UTF-8'
    response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'
    return response


def create_ical_entry (e, request):
        event = icalendar.Event()

        # TODO should we generate an UUID when creating the event?
        uid = u'%s@techism.de' % (str(e.id))
        event['uid'] = icalendar.vText(uid)
        event['dtstamp'] = icalendar.vDatetime(datetime.utcnow())

        # The sequence field must be incremented each time the event is modifed.
        # The trick here is to subtract the create TS from the modify TS and
        # use the difference as sequence.
        sequence = 0
        if e.date_time_created and e.date_time_modified:
            createTimestamp = time.mktime(e.get_date_time_created_utc().timetuple())
            modifyTimestamp = time.mktime(e.get_date_time_modified_utc().timetuple())
            sequence = modifyTimestamp - createTimestamp
        event['sequence'] = icalendar.vInt(sequence) + 1

        # created and last-modified
        if e.date_time_created:
            event['created'] = icalendar.vDatetime(e.get_date_time_created_utc())
        if e.date_time_modified:
            event['last-modified'] = icalendar.vDatetime(e.get_date_time_modified_utc())

        # TENTATIVE, CONFIRMED, CANCELLED
        if e.canceled:
            event['status'] = icalendar.vText(u'CANCELLED')
        else:
            event['status'] = icalendar.vText(u'CONFIRMED')

        relative_url = e.get_absolute_url()
        absolute_url = request.build_absolute_uri(relative_url)
        
        event['url'] = icalendar.vUri(absolute_url)

        if e.title:
            event['summary'] = icalendar.vText(e.title)

        description = u''
        if e.description:
            description += e.description
        if e.url:
            if len(description) > 0:
                description += u'\n\n'
            description += u'Event Webseite: ' + e.url
        if len(description) > 0:
            description += u'\n\n'
        description += u'Event bei Techism: ' + absolute_url
        event['description'] = icalendar.vText(description)

        if e.date_time_begin:
            event['dtstart'] = icalendar.vDatetime(e.get_date_time_begin_utc())
        if e.date_time_end:
            event['dtend'] = icalendar.vDatetime(e.get_date_time_end_utc())

        # geo value isn't used by iCal readers :-(
        # maybe a trick is to add the geo coordinates to the location field using the following format:
        # $latitude, $longitude ($name, $street, $city)
        if e.location:
            location = u'%s, %s, %s' % (e.location.name, e.location.street, e.location.city)
            event['location'] = icalendar.vText(location)
        if e.location and e.location.latitude and e.location.longitude:
            event['geo'] = icalendar.vGeo((e.location.latitude, e.location.longitude))

        return event
