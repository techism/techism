#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
import twitter


class TwitterTest(TestCase):

    fixtures = ['test-utils/fixture.json']
    
    def test_twitter(self):
	event_list = twitter.get_short_term_events()
        self.assertEqual(len(event_list), 2)
