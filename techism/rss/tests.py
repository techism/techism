#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.utils import timezone
import datetime
from techism.models import Event, Location
from django.core.cache import cache


class FeedTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    now_local = timezone.localtime(timezone.now())
    tomorrow_local = now_local + datetime.timedelta(days=1)
    tomorrow_190000 = tomorrow_local.replace(hour=19, minute=0, second=0).strftime("%d.%m.%Y %H:%M")
    tomorrow_180000 = tomorrow_local.replace(hour=18, minute=0, second=0).strftime("%d.%m.%Y %H:%M")

    def test_rss_upcomming_events(self):
        event = Event.objects.get(id=1)
        response = self.client.get('/feeds/rss/upcomming_events')
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/rss+xml; charset=utf-8')
        self.assertCacheHeaders(response)
        self.assertNotIn('Content-Security-Policy', response)
        self.assertIn("<rss xmlns:atom=\"http://www.w3.org/2005/Atom\" version=\"2.0\">", content)
        self.assertEqual(content.count("<item>"), 3)
        self.assertIn("<title>Future event with end date - %s</title>" % self.tomorrow_190000, content)
        self.assertIn("<link>http://testserver%s</link>" % event.get_absolute_url(), content)
        self.assertIn("<guid>http://testserver%s</guid>" % event.get_absolute_url(), content)

    def test_atom_upcomming_events(self):
        event = Event.objects.get(id=1)
        response = self.client.get('/feeds/atom/upcomming_events')
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/atom+xml; charset=utf-8')
        self.assertCacheHeaders(response)
        self.assertNotIn('Content-Security-Policy', response)
        self.assertIn("<feed xmlns=\"http://www.w3.org/2005/Atom\" xml:lang=\"de-DE\">", content)
        self.assertEqual(content.count("<entry>"), 3)
        self.assertIn("<title>Future event with end date - %s</title>" % self.tomorrow_190000, content)
        self.assertIn("<link href=\"http://testserver%s\" rel=\"alternate\"></link>" % event.get_absolute_url(), content)
        self.assertIn("<id>http://testserver%s</id>" % event.get_absolute_url(), content)

    def test_atom_upcomming_events_with_tag(self):
        event = Event.objects.get(id=2)
        response = self.client.get('/feeds/atom/tags/python/upcomming_events')
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/atom+xml; charset=utf-8')
        self.assertCacheHeaders(response)
        self.assertNotIn('Content-Security-Policy', response)
        self.assertIn("<feed xmlns=\"http://www.w3.org/2005/Atom\" xml:lang=\"de-DE\">", content)
        self.assertEqual(content.count("<entry>"), 1)
        self.assertIn("<title>Future event without end date - %s</title>" % self.tomorrow_190000, content)
        self.assertIn("<link href=\"http://testserver%s\" rel=\"alternate\"></link>" % event.get_absolute_url(), content)
        self.assertIn("<id>http://testserver%s</id>" % event.get_absolute_url(), content)

    def test_atom_updated_event(self):
        # hack: save without change to create a version
        event = Event.objects.get(id=2)
        event.save()
        
        response = self.client.get('/feeds/atom/upcomming_events')
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.count("<entry>"), 3)
        self.assertIn("<title>Future event without end date - %s</title>" % self.tomorrow_190000, content)
        
        # change location, expect feed with updated location prefix
        event.location = Location.objects.get(id=2)
        event.save()
        cache.clear()
        
        response = self.client.get('/feeds/atom/upcomming_events')
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.count("<entry>"), 3)
        self.assertIn("<title>[Update][Ort] Future event without end date - %s</title>" % self.tomorrow_190000, content)
        
        # change start date, expect feed with updated date/time prefix
        event.date_time_begin = event.date_time_begin - datetime.timedelta(hours=1)
        event.save()
        cache.clear()
        
        response = self.client.get('/feeds/atom/upcomming_events')
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.count("<entry>"), 3)
        self.assertIn("<title>[Update][Datum] Future event without end date - %s</title>" % self.tomorrow_180000, content)
        
        # cancel event, expect feed with cancel prefix
        event.canceled = True;
        event.save()
        cache.clear()
        
        response = self.client.get('/feeds/atom/upcomming_events')
        content = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.count("<entry>"), 3)
        self.assertIn("<title>[Abgesagt] Future event without end date - %s</title>" % self.tomorrow_180000, content)
    
    def assertCacheHeaders(self, response):
        self.assertIn('ETag', response)
        self.assertIn('Expires', response)
        self.assertIn('Cache-Control', response)
        self.assertIn('max-age=60', response['Cache-Control'])
