#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import unittest
from techism import utils
import datetime

class Test(unittest.TestCase):

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
