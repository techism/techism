#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from techism.events.event_service import get_current_tags, get_upcomming_published_events_query_set, get_all_published_events_query_set

class EventServiceTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    
    def test_tags(self):
        it = get_current_tags().iterator()
        tag1 = it.next()
        self.assertEqual(tag1.name, "java")
        self.assertEqual(tag1.num_tags, 3)
        tag2 = it.next()
        self.assertEqual(tag2.name, "python")
        self.assertEqual(tag2.num_tags, 2)
        tag3 = it.next()
        self.assertEqual(tag3.name, "test")
        self.assertEqual(tag3.num_tags, 5)
        with self.assertRaises(StopIteration): 
            it.next()
            
    def test_upcomming_events(self):
        events = get_upcomming_published_events_query_set()
        self.assertEqual(events.count(), 5)
        
    def test_all_events(self):
        events = get_all_published_events_query_set()
        self.assertEqual(events.count(), 7)