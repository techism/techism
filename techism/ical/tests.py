#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.utils import timezone
from techism.ical import ical_service
from techism.models import Event
from django.test.client import RequestFactory
import datetime

class IcalServiceTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
        
    def test_create_calendar_with_metadata(self):
        event_list = [Event.objects.get(id=1), Event.objects.get(id=2)]
        request = RequestFactory().get('/feed.ics')
        entry = ical_service.create_calendar_with_metadata(event_list, request)
        ical_string = entry.as_string()
        self.assertIn("BEGIN:VCALENDAR", ical_string)
        self.assertIn("VERSION:2.0", ical_string)
        self.assertIn("PRODID:-//Techism//Techism//DE", ical_string)
        self.assertIn("X-WR-CALDESC:Techism - Events\, Projekte\, User Groups in München", ical_string)
        self.assertIn("X-WR-CALNAME:Techism", ical_string)
        self.assertIn("BEGIN:VEVENT", ical_string)
        self.assertEqual(ical_string.count("BEGIN:VEVENT"), 2)
        self.assertIn("UID:1@techism.de", ical_string)
        self.assertIn("UID:2@techism.de", ical_string)
        self.assertIn("END:VCALENDAR", ical_string)
    
    def test_create_ical_entry(self):
        now_local = timezone.localtime(timezone.now())
        tomorrow_local = now_local + datetime.timedelta(days=1)
        tomorrow_190000 = tomorrow_local.replace(hour=19, minute=0, second=0)
        tomorrow_190000_utc = tomorrow_190000.astimezone(timezone.utc)
        dtstart = tomorrow_190000_utc.strftime("%Y%m%dT%H%M%SZ")
        tomorrow_220000 = tomorrow_local.replace(hour=22, minute=0, second=0)
        tomorrow_220000_utc = tomorrow_220000.astimezone(timezone.utc)
        dtend = tomorrow_220000_utc.strftime("%Y%m%dT%H%M%SZ")
        
        event = Event.objects.get(id=1)
        request = RequestFactory().get('/feed.ics')
        entry = ical_service.create_ical_entry(event, request)
        ical_string = entry.as_string()
        self.assertIn("SUMMARY:Future event with end date", ical_string)
        self.assertIn("DTSTART:%s" % dtstart, ical_string)
        self.assertIn("DTEND:%s" % dtend, ical_string)
        self.assertIn("DTSTAMP:", ical_string)
        self.assertIn("UID:1@techism.de", ical_string)
        self.assertIn("SEQUENCE:", ical_string)
        self.assertIn("CREATED:20120923T145234Z", ical_string)
        self.assertIn("DESCRIPTION:", ical_string)
        self.assertIn("LAST-MODIFIED:20120923T145609Z", ical_string)
        self.assertIn("STATUS:CONFIRMED", ical_string)
        self.assertIn("URL:", ical_string)
        
    def test_create_ical_entry_with_multi_byte_chars(self):
        '''
        There are various bugs in icalendar regarding folding with multi-byte unicode characters.
        In various versions (2.1, 3.1) multi-byte characters are splitted in the middle.
        This test checks that multi-byte characters are not splitted in the middle and are not swallowed.
        '''
        self._create_ical_and_check_multi_byte_chars(u'')
        self._create_ical_and_check_multi_byte_chars(u'1')
        self._create_ical_and_check_multi_byte_chars(u'12')
        self._create_ical_and_check_multi_byte_chars(u'123')
        self._create_ical_and_check_multi_byte_chars(u'1234')

    def _create_ical_and_check_multi_byte_chars(self, prefix):
        event = Event(title=u'Test', description=prefix + u'ä' * 50)
        request = RequestFactory().get('/feed.ics')
        entry = ical_service.create_ical_entry(event, request)
        ical_string = entry.as_string()
        self.assertIn("ääää\r\n ääää", ical_string)
        self.assertEqual(ical_string.count("ä"), 50)


class IcalViewTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']

    def test_view_all(self):
        response = self.client.get('/feed.ics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/calendar; charset=UTF-8')
        self.assertEqual(response['Cache-Control'], 'public, must-revalidate, max-age=10800')
        self.assertIn('Expires', response)
        self.assertIn('Last-Modified', response)
        self.assertIn('ETag', response)
        self.assertIn("BEGIN:VCALENDAR", response.content)
        self.assertIn("BEGIN:VEVENT", response.content)
        self.assertEqual(response.content.count("BEGIN:VEVENT"), 4)
        self.assertIn("UID:1@techism.de", response.content)
        self.assertIn("UID:2@techism.de", response.content)
        self.assertIn("UID:5@techism.de", response.content)
        self.assertIn("UID:6@techism.de", response.content)

    def test_view_single_future_event(self):
        response = self.client.get('/ical/1.ics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/calendar; charset=UTF-8')
        self.assertEqual(response['Cache-Control'], 'public, must-revalidate, max-age=10800')
        self.assertIn('Expires', response)
        self.assertIn('Last-Modified', response)
        self.assertIn('ETag', response)
        self.assertIn("BEGIN:VCALENDAR", response.content)
        self.assertIn("BEGIN:VEVENT", response.content)
        self.assertEqual(response.content.count("BEGIN:VEVENT"), 1)
        self.assertIn("UID:1@techism.de", response.content)

    def test_view_single_past_event(self):
        response = self.client.get('/ical/4.ics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/calendar; charset=UTF-8')
        self.assertEqual(response['Cache-Control'], 'public, must-revalidate, max-age=31536000')
        self.assertIn('Expires', response)
        self.assertIn('Last-Modified', response)
        self.assertIn('ETag', response)
        self.assertIn("BEGIN:VCALENDAR", response.content)
        self.assertIn("BEGIN:VEVENT", response.content)
        self.assertEqual(response.content.count("BEGIN:VEVENT"), 1)
        self.assertIn("UID:4@techism.de", response.content)

    def test_view_single_nonexisting_event(self):
        response = self.client.get('/ical/1234567890.ics')
        self.assertEqual(response.status_code, 404)