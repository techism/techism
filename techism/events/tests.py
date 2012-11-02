#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from event_service import get_current_tags, get_upcomming_published_events_query_set
from techism.models import Event


class EventTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    
    def test_tags(self):
        it = get_current_tags()
        tag1 = it.next()
        self.assertEqual(tag1.name, "java")
        self.assertEqual(tag1.num_tags, 1)
        tag2 = it.next()
        self.assertEqual(tag2.name, "python")
        self.assertEqual(tag2.num_tags, 1)
        tag3 = it.next()
        self.assertEqual(tag3.name, "test")
        self.assertEqual(tag3.num_tags, 2)
        with self.assertRaises(StopIteration): 
            it.next()
            
    def test_upcomming_events(self):
        events = get_upcomming_published_events_query_set()
        self.assertEqual(events.count(), 2)

    def test_view_index_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(response.context['event_list']().count(), 2)
        self.assertIsNotNone(response.context['tags'])

    def test_view_index(self):
        response = self.client.get('/events/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event_list'])
        self.assertEqual(response.context['event_list']().count(), 2)
        self.assertIsNotNone(response.context['tags'])
        
    def test_view_details(self):
        response = self.client.get('/events/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event'])
        self.assertEqual(response.context['event'], Event.objects.get(id=1))
        self.assertIsNotNone(response.context['tags'])

    def test_view_details_slugified(self):
        response = self.client.get('/events/a-b-c-1/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['event'])
        self.assertEqual(response.context['event'], Event.objects.get(id=1))
        self.assertIsNotNone(response.context['tags'])
        
        