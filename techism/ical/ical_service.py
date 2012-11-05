#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import icalendar
import time


def create_calendar_with_metadata (event_list, request):
    cal = icalendar.Calendar()
    cal['prodid'] = icalendar.vText(u'-//Techism//Techism//DE')
    cal['version'] = icalendar.vText(u'2.0')
    cal['x-wr-calname'] = icalendar.vText(u'Techism')
    cal['x-wr-caldesc'] = icalendar.vText(u'Techism - Events, Projekte, User Groups in München')
    for e in event_list:
        event = create_ical_entry(e, request)
        cal.add_component(event)
    return cal


def create_ical_entry (event, request):
        entry = icalendar.Event()

        # TODO should we generate an UUID when creating the entry?
        uid = u'%s@techism.de' % (str(event.id))
        entry['uid'] = icalendar.vText(uid)
        entry['dtstamp'] = icalendar.vDatetime(datetime.utcnow())

        # The sequence field must be incremented each time the entry is modifed.
        # The trick here is to subtract the create TS from the modify TS and
        # use the difference as sequence.
        sequence = 0
        if event.date_time_created and event.date_time_modified: 
            create_timestamp = time.mktime(event.date_time_created.timetuple())
            modify_timestamp = time.mktime(event.date_time_modified.timetuple())
            sequence = modify_timestamp - create_timestamp
        entry['sequence'] = icalendar.vInt(sequence) + 1

        # created and last-modified
        if event.date_time_created:
            entry['created'] = icalendar.vDatetime(event.date_time_created)
        if event.date_time_modified:
            entry['last-modified'] = icalendar.vDatetime(event.date_time_modified)

        # TENTATIVE, CONFIRMED, CANCELLED
        if event.canceled:
            entry['status'] = icalendar.vText(u'CANCELLED')
        else:
            entry['status'] = icalendar.vText(u'CONFIRMED')

        relative_url = event.get_absolute_url()
        absolute_url = request.build_absolute_uri(relative_url)
        
        entry['url'] = icalendar.vUri(absolute_url)

        if event.title:
            entry['summary'] = icalendar.vText(event.title)

        description = u''
        if event.description:
            description += event.description
        if event.url:
            if len(description) > 0:
                description += u'\n\n'
            description += u'Event Webseite: ' + event.url
        if len(description) > 0:
            description += u'\n\n'
        description += u'Event bei Techism: ' + absolute_url
        entry['description'] = icalendar.vText(description)

        if event.date_time_begin:
            entry['dtstart'] = icalendar.vDatetime(event.date_time_begin)
        if event.date_time_end:
            entry['dtend'] = icalendar.vDatetime(event.date_time_end)

        # geo value isn't used by iCal readers :-(
        # maybe a trick is to add the geo coordinates to the location field using the following format:
        # $latitude, $longitude ($name, $street, $city)
        if event.location:
            location = u'%s, %s, %s' % (event.location.name, event.location.street, event.location.city)
            entry['location'] = icalendar.vText(location)
        if event.location and event.location.latitude and event.location.longitude:
            entry['geo'] = icalendar.vGeo((event.location.latitude, event.location.longitude))

        return entry
