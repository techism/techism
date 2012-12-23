#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
import organization_service

class OrganizationServiceTest(TestCase):

    fixtures = ['test-utils/fixture.json']
    
    def test_get_all(self):
        organizations_list = organization_service.get_all()
        self.assertEqual(len(organizations_list), 2)
        
    def test_get_current_tags(self):
        tags = organization_service.get_tags()
        tag1 = tags.next()
        self.assertEqual(tag1.name, "tag1")
        self.assertEqual(tag1.num_tags, 2)
        tag2 = tags.next()
        self.assertEqual(tag2.name, "tag2")
        self.assertEqual(tag2.num_tags, 1)


class OrganizationViewsTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    
    def test_index_view(self):
        response = self.client.get('/orgs/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['organization_list'])
        self.assertEqual(len(response.context['organization_list']), 2)
        
    def test_index_view_tag(self):
        response = self.client.get('/orgs/tags/tag1/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['organization_list'])
        self.assertEqual(len(response.context['organization_list']), 2)