#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from event_service import get_current_tags, get_upcomming_published_events_query_set
from techism.models import Event, EventTag
from templatetags import web_tags
import pytz
import datetime
from django.utils import timezone
from forms import EventForm, CommaSeparatedTagsFormField
from django.core.exceptions import ValidationError
import json


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

    def test_view_get_locations(self):
        response = self.client.get('/events/locations/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(1, len(data))
        self.assertEqual(6, len(data[0]))
        self.assertDictEqual({
                              u'id': u'1',
                              u'name': u'Stadtverwaltung',
                              u'street': u'Marienplatz',
                              u'city': u'80331 München',
                              u'latitude': u'48.13788',
                              u'longitude': u'11.575953'
                              }, data[0])
        
        

class EventFormsTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    
    def test_comma_separated_tags_form_field_is_required(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        try:
            field.clean("")
            self.fail("Must throw ValidationError")
        except ValidationError:
            pass
        
    def test_comma_separated_tags_form_field_existing_tags(self):
        python = EventTag.objects.get(name="python")
        java = EventTag.objects.get(name="java")
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        tags = field.clean("python, java")
        self.assertItemsEqual((python,java), tags)
        self.assertEqual(4, EventTag.objects.count())
        
    def test_comma_separated_tags_form_field_new_tags(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        tags = field.clean("foo, bar")
        self.assertEquals(2, len(tags))
        self.assertEqual(tags[0], EventTag.objects.get(name="foo"))
        self.assertEqual(tags[1], EventTag.objects.get(name="bar"))
        self.assertEqual(6, EventTag.objects.count())
        
    def test_comma_separated_tags_form_field_strip_lowercase_filter_empty_and_duplicates(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        tags = field.clean("foo, , Foo Bar,, bar, FOO ,")
        self.assertEquals(3, len(tags))
        self.assertEqual(tags[0], EventTag.objects.get(name="foo"))
        self.assertEqual(tags[1], EventTag.objects.get(name="foo bar"))
        self.assertEqual(tags[2], EventTag.objects.get(name="bar"))
        self.assertEqual(7, EventTag.objects.count())

    def test_comma_separated_tags_form_field_allowed_characters(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        tags = field.clean("foo, a_z-0.9 äöüß")
        self.assertEquals(2, len(tags))
        self.assertEqual(tags[0], EventTag.objects.get(name="foo"))
        self.assertEqual(tags[1], EventTag.objects.get(name="a_z-0.9 äöüß"))
        self.assertEqual(6, EventTag.objects.count())

    def test_comma_separated_tags_form_field_not_allowed_characters(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        try:
            field.clean("foo, <script>")
            self.fail("Must throw ValidationError")
        except ValidationError:
            pass
        

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
    
