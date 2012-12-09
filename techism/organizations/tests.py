#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
import organization_service

class OrganizationServiceTest(TestCase):

    fixtures = ['test-utils/fixture.json']
    
    def test_get_all(self):
        organizations_list = organization_service.get_all()
        self.assertEqual(len(organizations_list), 2)
