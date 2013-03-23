#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from techism.events.templatetags import web_tags
import pytz
import datetime
from django.utils import timezone


class WebTagsTest(TestCase):

    def test_yesterday(self):
        tomorrow_local = timezone.localtime(timezone.now()) + datetime.timedelta(days=-1)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertNotIn(u'Heute', display)
        self.assertNotIn(u'Morgen', display)
        self.assertNotIn(u'Übermorgen', display)
    
    def test_today(self):
        today_local = timezone.localtime(timezone.now())
        today_utc = today_local.astimezone(pytz.utc)
        display = web_tags.display_date(today_utc)
        self.assertIn("Heute", display)
        
        today_local = today_local.replace(hour=0, minute=0, second=0)
        today_utc = today_local.astimezone(pytz.utc)
        display = web_tags.display_date(today_utc)
        self.assertIn(u"Heute", display)

        today_local = today_local.replace(hour=23, minute=59, second=59)
        today_utc = today_local.astimezone(pytz.utc)
        display = web_tags.display_date(today_utc)
        self.assertIn(u'Heute', display)
        
    
    def test_tomorrow(self):
        tomorrow_local = timezone.localtime(timezone.now()) + datetime.timedelta(days=1)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Morgen', display)
        
        tomorrow_local = tomorrow_local.replace(hour=0, minute=0, second=0)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Morgen', display)

        tomorrow_local = tomorrow_local.replace(hour=23, minute=59, second=59)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Morgen', display)
        
        
    def test_day_after_tomorrow(self):
        tomorrow_local = timezone.localtime(timezone.now()) + datetime.timedelta(days=2)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Übermorgen', display)

        tomorrow_local = tomorrow_local.replace(hour=0, minute=0, second=0)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Übermorgen', display)
        
        tomorrow_local = tomorrow_local.replace(hour=23, minute=59, second=59)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertIn(u'Übermorgen', display)

    
    def test_three_days(self):
        tomorrow_local = timezone.localtime(timezone.now()) + datetime.timedelta(days=3)
        tomorrow_utc = tomorrow_local.astimezone(pytz.utc)
        display = web_tags.display_date(tomorrow_utc)
        self.assertNotIn(u'Heute', display)
        self.assertNotIn(u'Morgen', display)
        self.assertNotIn(u'Übermorgen', display)
    
