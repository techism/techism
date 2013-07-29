#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.test import TestCase
from techism.csv.management.commands import event_export_csv
import csv


class EventExportCsvUnitTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    
    def test_command(self):
        cmd = event_export_csv.Command()
        cmd.handle()
        
        filename = os.path.join(settings.STATIC_ROOT, 'export', 'techism-events.csv')
        self.assertTrue(os.path.exists(filename), 'Export file was not generated: %s' % filename)
        f = open(filename, 'r')
        reader = csv.DictReader(f)
        self.assertEqual(reader.fieldnames, ['title', 'date_time_begin', 'date_time_end', 'url', 'location_name', 'location_lat', 'location_lng', 'tags'])
        self.assertEqual(len(list(reader)), 8)

