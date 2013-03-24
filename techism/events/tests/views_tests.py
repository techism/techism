#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.utils import timezone
import json
import reversion
import datetime
from techism.models import Event, EventTag, Location

class EventViewsTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']

    def assertCacheHeaders(self, response):
        self.assertIn('ETag', response)
        self.assertIn('Expires', response)
        self.assertIn('Cache-Control', response)
        self.assertIn('max-age=60', response['Cache-Control'])

    def test_index_view_root(self):
        url = '/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 5)
        self.assertIsNotNone(response.context['tags'])
        self.assertTrue(len(response.context['event_list']) > 0)

    def test_index_view(self):
        url = '/events/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 5)
        self.assertIsNotNone(response.context['tags'])
        self.assertTrue(len(response.context['event_list']) > 0)

    def test_year_view_with_current_year(self):
        current_year = str(timezone.localtime(timezone.now()).year)
        url = '/events/' + current_year + '/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 7)
        self.assertIsNotNone(response.context['tags'])

    def test_year_view_with_2011(self):
        url = '/events/2011/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 0)
        self.assertIsNotNone(response.context['tags'])

    def test_year_view_with_current_year_and_tag(self):
        current_year = str(timezone.localtime(timezone.now()).year)
        url = '/events/' + current_year + '/tags/python/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 2)
        self.assertIsNotNone(response.context['tags'])

    def test_year_view_with_current_year_and_nonexisting_tag(self):
        current_year = str(timezone.localtime(timezone.now()).year)
        url = '/events/' + current_year + '/tags/nonexistingtag/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 0)
        self.assertIsNotNone(response.context['tags'])
        self.assertIn('Keine Events vorhanden.', response.content)

    def test_year_month_view(self):
        today = timezone.localtime(timezone.now())
        year, month, day = today.timetuple()[:3]
        new_month = month - 1
        new_date = today.replace(year= year + (new_month / 12), month=new_month % 12)
        url = '/events/' + str(new_date.year) + '/' + str(new_date.month) + '/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 1)
        self.assertIsNotNone(response.context['tags'])

    def test_year_month_day_view(self):
        today = timezone.localtime(timezone.now())
        yesterday = today + datetime.timedelta(days=-1)
        year = str(yesterday.year)
        month = str(yesterday.month)
        day = str(yesterday.day)
        url = '/events/' + year + '/' + month + '/' + day + '/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 2)
        self.assertIsNotNone(response.context['tags'])

    def test_tags_view_with_events(self):
        url = '/events/tags/python/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 2)
        self.assertIsNotNone(response.context['tags'])
        self.assertTrue(len(response.context['event_list']) > 0)

    def test_tags_view_without_events(self):
        url = '/events/tags/tagwithoutevent/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(len(response.context['event_list']), 0)
        self.assertIsNotNone(response.context['tags'])
        self.assertTrue(len(response.context['event_list']) == 0)
        self.assertIn('Keine Events vorhanden.', response.content)

    def test_tags_view_of_nonexisting_tag(self):
        response = self.client.get('/events/tags/nonexistingtag/')
        self.assertEqual(response.status_code, 404)

    def test_details_view(self):
        url = '/events/1/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event'])
        self.assertEqual(response.context['event'], Event.objects.get(id=1))
        self.assertIsNotNone(response.context['tags'])
        self.assertIn("Morgen", response.content)
        self.assertIn("webcal://testserver/ical/1.ics", response.content)

    def test_details_view_slugified(self):
        url = '/events/a-b-c-1/'
        response = self.__get_response_and_check_headers(url)
        self.assertIsNotNone(response.context['event'])
        self.assertEqual(response.context['event'], Event.objects.get(id=1))
        self.assertIsNotNone(response.context['tags'])
        self.assertIn("Morgen", response.content)
        self.assertIn("webcal://testserver/ical/1.ics", response.content)

    def test_details_view_with_nonexisting_event(self):
        response = self.client.get('/events/1234567890/')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Content-Security-Policy', response)

    def test_details_view_with_nondigit_event_id(self):
        response = self.client.get('/events/abc/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/events/tags/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/events/favicon.ico/')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/events/abc-123/wp-content/themes/modularity/includes/timthumb.php/')
        self.assertEqual(response.status_code, 404)

    def test_locations_view(self):
        url = '/events/locations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertCacheHeaders(response)
        data = json.loads(response.content)
        self.assertEqual(2, len(data))
        self.assertEqual(6, len(data[0]))
        self.assertEqual(6, len(data[1]))
        self.assertIn("Stadtverwaltung", response.content)
        self.assertIn("Marienplatz", response.content)
        self.assertIn("80331 M\\u00fcnchen", response.content)
        self.assertIn("11.575953", response.content)
        self.assertIn("48.13788", response.content)

    def test_create_view_get(self):
        url = '/events/create/'
        response = self.__get_response_and_check_headers(url)
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
        
        # check revision was created
        version_list = reversion.get_for_object(event)
        self.assertEqual(2, len(version_list))
    
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
        
        # check revision was created
        version_list = reversion.get_for_object(event)
        self.assertEqual(2, len(version_list))

    def test_copy_view_get(self):
        response = self.client.get('/events/create/1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Security-Policy', response)
        self.assertCacheHeaders(response)
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

    def __get_response_and_check_headers (self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Security-Policy', response)
        self.assertCacheHeaders(response)
        return response