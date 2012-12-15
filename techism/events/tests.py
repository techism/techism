#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from event_service import get_current_tags, get_upcomming_published_events_query_set
from techism.models import Event, EventTag, Location
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

    def test_index_view_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 4)
        self.assertIsNotNone(response.context['tags'])

    def test_index_view(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 4)
        self.assertIsNotNone(response.context['tags'])

    def test_details_view(self):
        response = self.client.get('/events/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event'])
        self.assertEqual(response.context['event'], Event.objects.get(id=1))
        self.assertIsNotNone(response.context['tags'])
        self.assertIn("Morgen", response.content)
        self.assertIn("webcal://testserver/ical/1.ics", response.content)

    def test_details_view_slugified(self):
        response = self.client.get('/events/a-b-c-1/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event'])
        self.assertEqual(response.context['event'], Event.objects.get(id=1))
        self.assertIsNotNone(response.context['tags'])
        self.assertIn("Morgen", response.content)
        self.assertIn("webcal://testserver/ical/1.ics", response.content)

    def test_details_view_with_nonexisting_event(self):
        response = self.client.get('/events/1234567890/')
        self.assertEqual(response.status_code, 404)

    def test_locations_view(self):
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

    def test_create_view_get(self):
        response = self.client.get('/events/create/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="id_title"', response.content)
        self.assertIn('id="id_url"', response.content)
        self.assertIn('id="id_description"', response.content)
        self.assertIn('id="id_tags"', response.content)
        self.assertIn('id="id_date_time_begin_0"', response.content)
        self.assertIn('id="id_date_time_begin_1"', response.content)
        self.assertIn('id="id_date_time_end_0"', response.content)
        self.assertIn('id="id_date_time_end_1"', response.content)
        self.assertIn('id="id_location"', response.content)
        self.assertIn('id="id_location_name"', response.content)
        self.assertIn('id="id_location_street"', response.content)
        self.assertIn('id="id_location_city"', response.content)
        self.assertIn('id="id_location_latitude"', response.content)
        self.assertIn('id="id_location_longitude"', response.content)

    def test_create_view_post_with_empty_form(self):
        response = self.client.post('/events/create/')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'Dieses Feld ist zwingend erforderlich.')
        self.assertFormError(response, 'form', 'url', 'Dieses Feld ist zwingend erforderlich.')
        self.assertFormError(response, 'form', 'date_time_begin', 'Dieses Feld ist zwingend erforderlich.')
        self.assertFormError(response, 'form', 'tags', 'Dieses Feld ist zwingend erforderlich.')
        pass

    def test_create_view_post__create_new_unpublished_event_with_new_tags_and_new_location(self):
        num_events = Event.objects.count()
        num_tags = EventTag.objects.count()
        num_locations = Location.objects.count()
        
        data = {
                'title': 'Some Title',
                'url': 'http://www.example.com/5/',
                'description': 'Some Description',
                'tags': 'aaa,bbb,ccc',
                'date_time_begin_0': '01.01.2099',
                'date_time_begin_1': '18:00',
                'date_time_end_0': '01.01.2099',
                'date_time_end_1': '22:00',
                'location_name': 'Somewhere',
                'location_street': 'Somestreet 1',
                'location_city': '12345 Somecity',
                'location_latitude': '12.34567',
                'location_longitude': '23.45678',
                }
        response = self.client.post('/events/create/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # check object count in DB
        self.assertEqual(num_events + 1, Event.objects.count())
        self.assertEqual(num_tags + 3, EventTag.objects.count())
        self.assertEqual(num_locations + 1, Location.objects.count())
        
        # check that event was created
        event = Event.objects.get(title='Some Title')
        
        # check that tags were created
        tag1 = EventTag.objects.get(name='aaa')
        tag2 = EventTag.objects.get(name='bbb')
        tag3 = EventTag.objects.get(name='ccc')
        self.assertIn(tag1, event.tags.all())
        self.assertIn(tag2, event.tags.all())
        self.assertIn(tag3, event.tags.all())
        
        # check that location was created
        location = Location.objects.get(name='Somewhere')
        self.assertEqual(location, event.location)
        
        # check that event is not published
        self.assertFalse(event.published)
        self.assertIn('Dieses Event ist noch nicht veröffentlicht.', response.content)
    
    def test_create_view_post__create_new_unpublished_event_with_existing_tags_and_existing_location(self):
        num_events = Event.objects.count()
        num_tags = EventTag.objects.count()
        num_locations = Location.objects.count()
        
        data = {
                'title': 'Some Title',
                'url': 'http://www.example.com/5/',
                'description': 'Some Description',
                'tags': 'Java, Python',
                'date_time_begin_0': '01.01.2099',
                'date_time_begin_1': '18:00',
                'date_time_end_0': '01.01.2099',
                'date_time_end_1': '22:00',
                'location': '1',
                'location_name': 'Stadtverwaltung',
                'location_street': 'Marienplatz',
                'location_city': '80331 München',
                'location_latitude': '48.138',
                'location_longitude': '11.574',
                }
        response = self.client.post('/events/create/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # check object count in DB
        self.assertEqual(num_events + 1, Event.objects.count())
        self.assertEqual(num_tags + 0, EventTag.objects.count())
        self.assertEqual(num_locations + 0, Location.objects.count())
        
        # check that event was created
        event = Event.objects.get(title='Some Title')
        
        # check that existing tags is used
        tag1 = EventTag.objects.get(name='java')
        tag2 = EventTag.objects.get(name='python')
        self.assertIn(tag1, event.tags.all())
        self.assertIn(tag2, event.tags.all())
        
        # check that location is used and was updated
        location = Location.objects.get(name='Stadtverwaltung')
        self.assertEqual(48.138, location.latitude)
        self.assertEqual(11.574, location.longitude)
        self.assertEqual(location, event.location)
        
        # check that event is not published
        self.assertFalse(event.published)
        self.assertIn('Dieses Event ist noch nicht veröffentlicht.', response.content)

    def test_copy_view_get(self):
        response = self.client.get('/events/create/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="id_title"', response.content)
        self.assertIn('id="id_url"', response.content)
        self.assertIn('id="id_description"', response.content)
        self.assertIn('id="id_tags"', response.content)
        self.assertIn('id="id_date_time_begin_0"', response.content)
        self.assertIn('id="id_date_time_begin_1"', response.content)
        self.assertIn('id="id_date_time_end_0"', response.content)
        self.assertIn('id="id_date_time_end_1"', response.content)
        self.assertIn('id="id_location"', response.content)
        self.assertIn('id="id_location_name"', response.content)
        self.assertIn('id="id_location_street"', response.content)
        self.assertIn('id="id_location_city"', response.content)
        self.assertIn('id="id_location_latitude"', response.content)
        self.assertIn('id="id_location_longitude"', response.content)

    def test_edit_view_get_is_forbidden_for_unauthenticated_user(self):
        response = self.client.get('/events/edit/1', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_edit_view_post_is_forbidden_for_unauthenticated_user(self):
        response = self.client.post('/events/edit/1', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_cancel_view_get_is_forbidden_for_unauthenticated_user(self):
        response = self.client.get('/events/cancel/1', follow=True)
        self.assertEqual(response.status_code, 403)

    def test_cancel_view_post_is_forbidden_for_unauthenticated_user(self):
        response = self.client.post('/events/cancel/1', follow=True)
        self.assertEqual(response.status_code, 403)


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
        self.assertEqual(2, len(tags))
        self.assertEqual(tags[0], EventTag.objects.get(name="foo"))
        self.assertEqual(tags[1], EventTag.objects.get(name="bar"))
        self.assertEqual(6, EventTag.objects.count())
        
    def test_comma_separated_tags_form_field_strip_lowercase_filter_empty_and_duplicates(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        tags = field.clean("foo, , Foo Bar,, bar, FOO ,")
        self.assertEqual(3, len(tags))
        self.assertEqual(tags[0], EventTag.objects.get(name="foo"))
        self.assertEqual(tags[1], EventTag.objects.get(name="foo bar"))
        self.assertEqual(tags[2], EventTag.objects.get(name="bar"))
        self.assertEqual(7, EventTag.objects.count())

    def test_comma_separated_tags_form_field_allowed_characters(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        tags = field.clean("foo, a_z-0.9 äöüß")
        self.assertEqual(2, len(tags))
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
    
