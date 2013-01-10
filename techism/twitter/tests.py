#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from techism.models import Event, TweetedEvent, Location
import datetime
from django.test import TestCase
from django.utils import timezone
import twitter
import mock
from django.conf import settings


class TwitterIntegrationTest(TestCase):

    fixtures = ['test-utils/fixture.json']
    now_local = timezone.localtime(timezone.now())
    tomorrow_local = now_local + datetime.timedelta(days=1)
    nextweek_local = now_local + datetime.timedelta(days=7)
    tomorrow_190000 = tomorrow_local.replace(hour=19, minute=0, second=0)
    tomorrow_localtime = tomorrow_190000.strftime("%d.%m.%Y %H:%M")
    tomorrow_string = tomorrow_local.strftime("%d.%m.%Y")
    nextweek_string = nextweek_local.strftime("%d.%m.%Y")
    

    @mock.patch('techism.twitter.twitter.__tweet_event')
    def test_short_term_tweet_canceled_event(self, mocked_tweet_event_function):
        event1 = Event.objects.get(id=1)
        event1.canceled = True
        event1.save()
        
        event2 = Event.objects.get(id=2)
        event2.canceled = True
        event2.save()
        
        # tweet of first event
        twitter.tweet_upcoming_shortterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertTrue(mocked_tweet_event_function.call_args[0][0].startswith('[Abgesagt] '), 'Tweet must start with [Abgesagt]')
        mocked_tweet_event_function.reset_mock()
        
        # tweet of second event
        twitter.tweet_upcoming_shortterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertTrue(mocked_tweet_event_function.call_args[0][0].startswith('[Abgesagt] '), 'Tweet must start with [Abgesagt]')
        mocked_tweet_event_function.reset_mock()
        
        twitter.tweet_upcoming_shortterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        mocked_tweet_event_function.reset_mock()
        
        # no more tweets
        twitter.tweet_upcoming_shortterm_events()
        self.assertFalse(mocked_tweet_event_function.called)
        
    @mock.patch('techism.twitter.twitter.__tweet_event')
    def test_long_term_tweet_canceled_event(self, mocked_tweet_event_function):
        event1 = Event.objects.get(id=7)
        event1.canceled = True
        event1.save()
        
        # tweet of first event
        twitter.tweet_upcoming_longterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertTrue(mocked_tweet_event_function.call_args[0][0].startswith('[Abgesagt] '), 'Tweet must start with [Abgesagt]')
        mocked_tweet_event_function.reset_mock()
        
        # no more tweets
        twitter.tweet_upcoming_longterm_events()
        self.assertFalse(mocked_tweet_event_function.called)

    @mock.patch('techism.twitter.twitter.__tweet_event')
    def test_short_term_tweet_updated_event(self, mocked_tweet_event_function):
        # tweet events, without prefix
        twitter.tweet_upcoming_shortterm_events()
        twitter.tweet_upcoming_shortterm_events()
        mocked_tweet_event_function.reset_mock()

        # hack: save without change to create a version
        event = Event.objects.get(id=2)
        event.save()
        
        # change start date, expect tweet with updated date/time
        event.date_time_begin = event.date_time_begin - datetime.timedelta(hours=1)
        event.save()
        
        twitter.tweet_upcoming_shortterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertTrue(mocked_tweet_event_function.call_args[0][0].startswith('[Update][Datum] Future event'), 'Tweet must start with [Update][Datum]')
        mocked_tweet_event_function.reset_mock()
        
        # change location, expect tweet with updated location
        event.location = Location.objects.get(id=2)
        event.save()
        
        twitter.tweet_upcoming_shortterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertTrue(mocked_tweet_event_function.call_args[0][0].startswith('[Update][Ort] Future event'), 'Tweet must start with [Update][Ort]')
        mocked_tweet_event_function.reset_mock()
        
        # cancel event, expect tweet with cancel info
        event.canceled = True;
        event.save()
        
        twitter.tweet_upcoming_shortterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertTrue(mocked_tweet_event_function.call_args[0][0].startswith('[Abgesagt] Future event'), 'Tweet must start with [Abgesagt]')
        mocked_tweet_event_function.reset_mock()
        
        twitter.tweet_upcoming_shortterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        mocked_tweet_event_function.reset_mock()
        
        # no more tweet
        twitter.tweet_upcoming_shortterm_events()
        self.assertFalse(mocked_tweet_event_function.called)
        
    @mock.patch('techism.twitter.twitter.__tweet_event')
    def test_long_term_tweet_updated_event(self, mocked_tweet_event_function):
        # tweet events, without prefix
        twitter.tweet_upcoming_longterm_events()
        mocked_tweet_event_function.reset_mock()

        # hack: save without change to create a version
        event = Event.objects.get(id=7)
        event.save()
        
        # change start date, expect tweet with updated date/time
        event.date_time_begin = event.date_time_begin - datetime.timedelta(hours=1)
        event.save()
        
        twitter.tweet_upcoming_longterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertTrue(mocked_tweet_event_function.call_args[0][0].startswith('[Update][Datum] Future long term'), 'Tweet must start with [Update][Datum]')
        mocked_tweet_event_function.reset_mock()
        
        # change location, expect tweet with updated location
        event.location = Location.objects.get(id=2)
        event.save()
        
        twitter.tweet_upcoming_longterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertTrue(mocked_tweet_event_function.call_args[0][0].startswith('[Update][Ort] Future long term'), 'Tweet must start with [Update][Ort]')
        mocked_tweet_event_function.reset_mock()
        
        # cancel event, expect tweet with cancel info
        event.canceled = True;
        event.save()
        
        twitter.tweet_upcoming_longterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertTrue(mocked_tweet_event_function.call_args[0][0].startswith('[Abgesagt] Future long term'), 'Tweet must start with [Abgesagt]')
        mocked_tweet_event_function.reset_mock()
        
        # no more tweet
        twitter.tweet_upcoming_longterm_events()
        self.assertFalse(mocked_tweet_event_function.called)

    def test_get_short_term_events(self):
        event_list = twitter.get_short_term_events()
        self.assertEqual(len(event_list), 3)

    def test_get_long_term_events(self):
        event_list = twitter.get_long_term_events()
        self.assertEqual(len(event_list), 1)

    @mock.patch('techism.twitter.twitter.__tweet_event')
    def test_short_term_tweet_and_marked_as_tweeted(self, mocked_tweet_event_function):
        tweets = []
        
        # 1st call: one event is tweeted and marked
        twitter.tweet_upcoming_shortterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertEqual(TweetedEvent.objects.count(), 1)
        tweets.append(mocked_tweet_event_function.call_args[0][0])
        mocked_tweet_event_function.reset_mock()
        
        # 2nd call: other event is tweeted and marked
        twitter.tweet_upcoming_shortterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertEqual(TweetedEvent.objects.count(), 2)
        tweets.append(mocked_tweet_event_function.call_args[0][0])
        mocked_tweet_event_function.reset_mock()
        
        twitter.tweet_upcoming_shortterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertEqual(TweetedEvent.objects.count(), 3)
        tweets.append(mocked_tweet_event_function.call_args[0][0])
        mocked_tweet_event_function.reset_mock()
        
        # 4rd call: no more upcomming event
        twitter.tweet_upcoming_shortterm_events()
        self.assertFalse(mocked_tweet_event_function.called)
        
        # assert correct tweets
        event2 = Event.objects.get(id=2)
        event1 = Event.objects.get(id=1)
        self.assertIn(event1.title + ' - ' + self.tomorrow_localtime + ' ' + settings.HTTP_URL + event1.get_absolute_url(), tweets)
        self.assertIn(event2.title + ' - ' + self.tomorrow_localtime + ' ' + settings.HTTP_URL + event2.get_absolute_url(), tweets)


    @mock.patch('techism.twitter.twitter.__tweet_event')
    def test_long_term_tweet_and_marked_as_tweeted(self, mocked_tweet_event_function):
        tweets = []
        
        # 1st call: one event is tweeted and marked
        twitter.tweet_upcoming_longterm_events()
        self.assertEquals(1, mocked_tweet_event_function.call_count)
        self.assertEqual(TweetedEvent.objects.count(), 1)
        tweets.append(mocked_tweet_event_function.call_args[0][0])
        mocked_tweet_event_function.reset_mock()
        
        # 2. call: no more upcomming event
        twitter.tweet_upcoming_longterm_events()
        self.assertFalse(mocked_tweet_event_function.called)
        
        # assert correct tweets
        event = Event.objects.get(id=7)
        self.assertIn(event.title + ' - ' + self.tomorrow_string + '-' + self.nextweek_string + ' ' + settings.HTTP_URL + event.get_absolute_url(), tweets)


class TwitterUnitTest(TestCase):

    def test_format_tweet(self):
        event = Mock ()
        event.get_number_of_days = mock.Mock(return_value=0)
        now_utc = timezone.now()
        event.date_time_begin = now_utc
        event.get_absolute_url = mock.Mock(return_value='/events/java-event-1')
        event.title = 'Testevent'
        tweet = twitter.format_tweet(event, '')
        now_local = timezone.localtime(now_utc)
        now_local_str = now_local.strftime("%d.%m.%Y %H:%M")
        self.assertEqual(tweet, u'Testevent - ' + now_local_str + ' ' + settings.HTTP_URL + '/events/java-event-1')

class Mock(object):
    pass

