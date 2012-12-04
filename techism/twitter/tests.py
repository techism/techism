#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
import twitter
import mock


class TwitterTest(TestCase):

    fixtures = ['test-utils/fixture.json']
    
    ## Integration Tests

    def test_get_short_term_events(self):
        event_list = twitter.get_short_term_events()
        self.assertEqual(len(event_list), 2)

    ## Unit Tests

    def test_format_tweet(self):
        event = Mock ()
        event.takes_more_than_one_day = mock.Mock(return_value=False)
        now = timezone.localtime(timezone.now())
        now_str = now.strftime("%d.%m.%Y %H:%M")
        event.date_time_begin = now
        event.get_absolute_url = mock.Mock(return_value='/events/java-event-1')
        event.title = 'Testevent'
        tweet = twitter.format_tweet(event, '')
        self.assertEqual(tweet, u'Testevent - ' + now_str + ' http://localhost:8000/events/java-event-1')



class Mock(object):
    pass

