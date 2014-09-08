#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.utils import timezone
import json
from techism.models import Event, EventTag
from datetime import datetime
import base64

class ApiViewTest(TestCase):

    fixtures = ['test-utils/fixture.json']

    def test_csp_reporting(self):
        json_data = '''{"csp-report": {
            "document-uri": "http://example.com/signup.html",
            "referrer": "http://evil.example.net/haxor.html",
            "blocked-uri": "http://evil.example.net/injected.png",
            "violated-directive": "img-src *.example.com",
            "original-policy": "default-src 'self'; img-src 'self' *.example.com; report-uri /_/csp-reports"
                }
            }''';
        response = self.client.post('/api/csp/', json_data, content_type="application/json")
        self.assertEqual('', response.content)

    def test_get_year(self):
        current_year = str(timezone.localtime(timezone.now()).year)
        url = '/api/events/' + current_year + '/'
        response = self.__get_response(url)
        data = json.loads(response.content)
        self.assertEqual(5, len(data))

    def test_get_month(self):
        current_year = str(timezone.localtime(timezone.now()).year)
        current_month = str(timezone.localtime(timezone.now()).month)
        url = '/api/events/' + current_year + '/' + current_month + '/'
        response = self.__get_response(url)
        data = json.loads(response.content)
        self.assertEqual(5, len(data))

    def test_get_day(self):
        current_year = str(timezone.localtime(timezone.now()).year)
        current_month = str(timezone.localtime(timezone.now()).month)
        current_day = str(timezone.localtime(timezone.now()).day)
        url = '/api/events/' + current_year + '/' + current_month + '/' + current_day + '/'
        response = self.__get_response(url)
        data = json.loads(response.content)
        self.assertEqual(2, len(data))

    def __get_response(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return response

    event_simple = '''{
        "title": "Example event",
        "url": "http://example.com",
        "description": "Lorem ipsum...",
        "tags": ["aaa", "bbb", "ccc"],
        "date_time_begin": "2013-04-28 17:04",
        "date_time_end": "2013-04-28 18:34"
    }'''

    def test_create_unauthenticated(self):
        response = self.client.post('/api/events/', self.event_simple, content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response['WWW-Authenticate'], 'Basic realm="Techism"')

    def test_create_illegal_header(self):
        User.objects.create_user('testuser', 'testuser@example.com', 'secret')
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode('invalid'),
        }
        response = self.client.post('/api/events/', self.event_simple, content_type="application/json", **auth_headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response['WWW-Authenticate'], 'Basic realm="Techism"')

    def test_create_unauthorized(self):
        User.objects.create_user('testuser', 'testuser@example.com', 'secret')
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode('testuser:secret'),
        }
        response = self.client.post('/api/events/', self.event_simple, content_type="application/json", **auth_headers)
        self.assertEqual(response.status_code, 403)

    def test_create_without_location_authorized(self):
        # create user with use_api permission
        p = Permission.objects.get(codename='use_api')
        user = User.objects.create_user('testuser', 'testuser@example.com', 'secret')
        user.user_permissions.add(p)
        user.save()
        # create event
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode('testuser:secret'),
        }
        response = self.client.post('/api/events/', self.event_simple, content_type="application/json", **auth_headers)
        # assertions
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content)
        event_id = int(response.content)
        event = Event.objects.get(pk=event_id);
        self.assertTrue(event)
        self.assertEqual(event.title, 'Example event')
        self.assertEqual(event.description, 'Lorem ipsum...')
        self.assertEqual(event.url, 'http://example.com')
        self.assertEqual(event.date_time_begin, datetime(2013, 04, 28, 15, 04, 00, 000, timezone.utc))
        self.assertEqual(event.date_time_end, datetime(2013, 04, 28, 16, 34, 00, 000, timezone.utc))
        self.assertIn(EventTag.objects.get(name='aaa'), event.tags.all())
        self.assertIn(EventTag.objects.get(name='bbb'), event.tags.all())
        self.assertIn(EventTag.objects.get(name='ccc'), event.tags.all())
        self.assertFalse(event.location)
        self.assertEqual(event.user, user)
        self.assertEqual(event.published, False)
        self.assertEqual(event.canceled, False)
        self.assertTrue(event.date_time_created)
        self.assertTrue(event.date_time_modified)
        self.assertFalse(event.organization)

