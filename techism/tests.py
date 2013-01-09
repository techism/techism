#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from techism import utils
from techism.models import Event, Location
import datetime
from django.utils import timezone
from django.conf import settings
from urlparse import urlparse
import reversion

class ModelsUnitTest(TestCase):
    
    def test_get_number_of_days_with_no_end_date(self):
        event = Event(date_time_begin = datetime.datetime(2012, 1, 1, 19, 0, 0, 0, timezone.utc))
        self.assertEqual(0, event.get_number_of_days())

    def test_get_number_of_days_with_end_date_within_24_hours(self):
        event = Event(date_time_begin = datetime.datetime(2012, 1, 1, 19, 0, 0, 0, timezone.utc),
                      date_time_end = datetime.datetime(2012, 1, 1, 22, 0, 0, 0, timezone.utc))
        self.assertEqual(0, event.get_number_of_days())
        event = Event(date_time_begin = datetime.datetime(2012, 1, 1, 19, 0, 0, 0, timezone.utc),
                      date_time_end = datetime.datetime(2012, 1, 2, 18, 30, 0, 0, timezone.utc))
        self.assertEqual(0, event.get_number_of_days())
        
    def test_get_number_of_days_with_end_date_more_than_24_hours(self):
        event = Event(date_time_begin = datetime.datetime(2012, 1, 1, 19, 0, 0, 0, timezone.utc),
                      date_time_end = datetime.datetime(2012, 1, 2, 19, 0, 0, 0, timezone.utc))
        self.assertEqual(1, event.get_number_of_days())
        event = Event(date_time_begin = datetime.datetime(2012, 1, 1, 19, 0, 0, 0, timezone.utc),
                      date_time_end = datetime.datetime(2012, 1, 2, 22, 00, 0, 0, timezone.utc))
        self.assertEqual(1, event.get_number_of_days())
        event = Event(date_time_begin = datetime.datetime(2012, 1, 1, 19, 0, 0, 0, timezone.utc),
                      date_time_end = datetime.datetime(2012, 1, 5, 22, 00, 0, 0, timezone.utc))
        self.assertEqual(4, event.get_number_of_days())
        

    def _test_tz(self):
        now = datetime.datetime.utcnow()
        print now
        print now.tzinfo
        now = timezone.now()
        print now
        print now.tzinfo


class ModelsIntegrationTest(TestCase):
    
    def test_event_versioning(self):
        now = timezone.now().replace(microsecond=0)
        tomorrow = now + datetime.timedelta(days=1)
        
        event = Event(title=u'Test', description='Test', url='http://www.example.com',
                      date_time_begin=now)
        event.save()
        
        version_list = reversion.get_for_object(event)
        self.assertEqual(1, len(version_list))
        
        event.date_time_begin=tomorrow
        event.save()
        
        version_list = reversion.get_for_object(event)
        self.assertEqual(2, len(version_list))
        self.assertEqual(now, version_list[1].field_dict['date_time_begin'])
        self.assertEqual(tomorrow, version_list[0].field_dict['date_time_begin'])


class UtilsTest(TestCase):

    def test_localize_none(self):
        dt = None
        result = utils.localize_to_utc(dt)
        self.assertIsNone(result)

    def test_localize_without_timezone_should_add_utc_timezone(self):
        dt = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, None)
        result = utils.localize_to_utc(dt)
        self.assertEqual(result, datetime.datetime(1970, 1, 1, 0, 0, 0, 0, utils.utc))
        self.assertEqual(result.tzinfo, utils.utc)

    def test_localize_with_cet_timezone_should_convert_to_utc_timezone(self):
        dt = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, utils.cet)
        result = utils.localize_to_utc(dt)
        self.assertEqual(result, datetime.datetime(1969, 12, 31, 23, 0, 0, 0, utils.utc))
        self.assertEqual(result.tzinfo, utils.utc)

    def test_cet_to_utc(self):
        dt = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, None)
        result = utils.cet_to_utc(dt)
        self.assertEqual(result, datetime.datetime(1969, 12, 31, 23, 0, 0, 0, utils.utc))
        self.assertEqual(result.tzinfo, utils.utc)

    def test_utc_to_cet(self):
        dt = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, None)
        result = utils.utc_to_cet(dt)
        self.assertEqual(result, datetime.datetime(1970, 1, 1, 1, 0, 0, 0, utils.cet))
        self.assertEqual(result.tzinfo, utils.cet)

    def test_slugify(self):
        slugified = utils.slugify(u'A string with\twhitespace, UPPER CASE, unicode (ä), under_score _.')
        self.assertEqual(slugified, "a-string-with-whitespace-upper-case-unicode-a-under_score-_")


class UtilsIntegrationTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    
    def test_event_versioning(self):
        
        now = timezone.now()
        t1 = now + datetime.timedelta(days=3)
        t2 = now + datetime.timedelta(days=5)
        
        # just created event, empty prefix expected
        event = Event(title=u'Test', description='Test', url='http://www.example.com', date_time_begin=t1)
        event.save()
        
        changed, prefix = utils.get_changed_and_change_prefix(event, now)
        self.assertFalse(changed)
        self.assertEqual("", prefix)
        
        # date updated, prefix expected
        now = timezone.now()
        event.date_time_begin = t2
        event.save()
        
        changed, prefix = utils.get_changed_and_change_prefix(event, now)
        self.assertTrue(changed)
        self.assertEqual("[Update][Datum] ", prefix)
        
        # location added, no update expected
        now = timezone.now()
        event.location = Location.objects.get(id=1)
        event.save()
        
        changed, prefix = utils.get_changed_and_change_prefix(event, now)
        self.assertFalse(changed)
        self.assertEqual("", prefix)
        
        # location updated, prefix expected
        now = timezone.now()
        event.location = Location.objects.get(id=2)
        event.save()
        
        changed, prefix = utils.get_changed_and_change_prefix(event, now)
        self.assertTrue(changed)
        self.assertEqual("[Update][Ort] ", prefix)
        
        # canceled, prefix expected
        now = timezone.now()
        event.canceled = True;
        event.save()
        
        changed, prefix = utils.get_changed_and_change_prefix(event, now)
        self.assertTrue(changed)
        self.assertEqual("[Abgesagt] ", prefix)


class AccountsViewsTest(TestCase):
    
    def test_login_view(self):
        response = self.client.get('/accounts/login/', follow=True)
        
        # if secure path is configured a redirect to https:// is expected
        if settings.HTTPS_PATHS and '/accounts/' in settings.HTTPS_PATHS:
            self.assertTrue(response.redirect_chain)
            self.assertEqual(1, len(response.redirect_chain))
            self.assertIn('https://', response.redirect_chain[0][0])
            self.assertEquals(302, response.redirect_chain[0][1])
        
        # check to result
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login mit Google", response.content)
        self.assertIn("Login mit Twitter", response.content)
        self.assertIn("Login mit Yahoo", response.content)
        self.assertIn("Login mit OpenID", response.content)
        
    def test_logout_view(self):
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertTrue(response.redirect_chain)
        self.assertEqual(response.status_code, 200)
        target_url = response.redirect_chain[-1][0]
        url = urlparse(target_url)
        self.assertEqual('/', url.path)
     
