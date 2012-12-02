#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from techism import utils
from techism.models import Event
import datetime
from django.utils import timezone

class ModelsTest(TestCase):
    
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
        from django.utils import timezone
        now = timezone.now()
        print now
        print now.tzinfo

    
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
        slugified = utils.slugify(u'A string with\twhitespace, upper case, unicode (ä).')
        self.assertEqual(slugified, "a-string-with-whitespace-upper-case-unicode-a")


class AccountsViewsTest(TestCase):
    
    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login mit Google", response.content)
        self.assertIn("Login mit Twitter", response.content)
        self.assertIn("Login mit Yahoo", response.content)
        self.assertIn("Login mit OpenID", response.content)
        
    def test_logout_view(self):
        response = self.client.get('/accounts/logout/')
        self.assertRedirects(response, '/')
     
