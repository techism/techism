#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
import json
from techism.events import json_service

class EventServiceTest(TestCase):

	fixtures = ['test-utils/fixture.json']

	#def test_get_event_from_json(self):
	#	json = '''[{ "description": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy..."}]'''
    #    event = json_service.get_event_from_json(json)
    #    self.assertEqual(event.canceled, false)
    #    self.assertEqual(event.url, "http://example.com")