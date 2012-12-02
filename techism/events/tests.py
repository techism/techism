#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from event_service import get_current_tags, get_upcomming_published_events_query_set
from techism.models import Event
from templatetags import web_tags
import pytz
import datetime
from django.utils import timezone
from techism import utils


class EventServiceTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    
    def test_tags(self):
        it = get_current_tags()
        tag1 = it.next()
        self.assertEqual(tag1.name, "java")
        self.assertEqual(tag1.num_tags, 2)
        tag2 = it.next()
        self.assertEqual(tag2.name, "python")
        self.assertEqual(tag2.num_tags, 2)
        tag3 = it.next()
        self.assertEqual(tag3.name, "test")
        self.assertEqual(tag3.num_tags, 4)
        with self.assertRaises(StopIteration): 
            it.next()
            
    def test_upcomming_events(self):
        events = get_upcomming_published_events_query_set()
        self.assertEqual(events.count(), 4)


class EventViewsTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']

    def test_view_index_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(response.context['event_list'].count(), 4)
        self.assertIsNotNone(response.context['tags'])

    def test_view_index(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(response.context['event_list'].count(), 4)
        self.assertIsNotNone(response.context['tags'])

    def test_view_details(self):
        response = self.client.get('/events/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event'])
        self.assertEqual(response.context['event'], Event.objects.get(id=1))
        self.assertIsNotNone(response.context['tags'])
        self.assertIn("Morgen", response.content)
        self.assertIn("webcal://testserver/ical/1.ics", response.content)

    def test_view_details_slugified(self):
        response = self.client.get('/events/a-b-c-1/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event'])
        self.assertEqual(response.context['event'], Event.objects.get(id=1))
        self.assertIsNotNone(response.context['tags'])
        self.assertIn("Morgen", response.content)
        self.assertIn("webcal://testserver/ical/1.ics", response.content)

    def test_view_details_of_nonexisting_event(self):
        response = self.client.get('/events/1234567890/')
        self.assertEqual(response.status_code, 404)

class WebTagsTest(TestCase):

    def test_yesterday(self):
        tomorrow_local = timezone.localtime(timezone.now()) + datetime.timedelta(days=-1)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertNotIn(u'Heute', display)
        self.assertNotIn(u'Morgen', display)
        self.assertNotIn(u'Übermorgen', display)
    
    def test_today(self):
        today_local = timezone.localtime(timezone.now())
        today_utc = today_local.astimezone(pytz.utc)
        display = web_tags.display_date(today_utc)
        self.assertIn("Heute", display)
        
        today_local = today_local.replace(hour=0, minute=0, second=0)
        today_utc = today_local.astimezone(pytz.utc)
        display = web_tags.display_date(today_utc)
        self.assertIn(u"Heute", display)

        today_local = today_local.replace(hour=23, minute=59, second=59)
        today_utc = today_local.astimezone(pytz.utc)
        display = web_tags.display_date(today_utc)
        self.assertIn(u'Heute', display)
        
    
    def test_tomorrow(self):
        tomorrow_local = timezone.localtime(timezone.now()) + datetime.timedelta(days=1)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Morgen', display)
        
        tomorrow_local = tomorrow_local.replace(hour=0, minute=0, second=0)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Morgen', display)

        tomorrow_local = tomorrow_local.replace(hour=23, minute=59, second=59)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Morgen', display)
        
        
    def test_day_after_tomorrow(self):
        tomorrow_local = timezone.localtime(timezone.now()) + datetime.timedelta(days=2)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Übermorgen', display)

        tomorrow_local = tomorrow_local.replace(hour=0, minute=0, second=0)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Übermorgen', display)
        
        tomorrow_local = tomorrow_local.replace(hour=23, minute=59, second=59)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Übermorgen', display)

    
    def test_three_days(self):
        tomorrow_local = timezone.localtime(timezone.now()) + datetime.timedelta(days=3)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertNotIn(u'Heute', display)
        self.assertNotIn(u'Morgen', display)
        self.assertNotIn(u'Übermorgen', display)
    