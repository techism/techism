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
        tags = organization_service.get_tags().iterator()
        tag1 = tags.next()
        self.assertEqual(tag1.name, "tag1")
        self.assertEqual(tag1.num_tags, 2)
        tag2 = tags.next()
        self.assertEqual(tag2.name, "tag2")
        self.assertEqual(tag2.num_tags, 1)


class OrganizationViewsTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    
    def assertCacheHeaders(self, response):
        self.assertIn('ETag', response)
        self.assertIn('Expires', response)
        self.assertIn('Cache-Control', response)
        self.assertIn('max-age=60', response['Cache-Control'])

    def test_index_view(self):
        response = self.client.get('/orgs/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Security-Policy', response)
        self.assertCacheHeaders(response)
        self.assertIsNotNone(response.context['organization_list'])
        self.assertEqual(len(response.context['organization_list']), 2)
        self.assertIsNotNone(response.context['tags'])

    def test_index_view_tag(self):
        response = self.client.get('/orgs/tags/tag1/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Security-Policy', response)
        self.assertCacheHeaders(response)
        self.assertIsNotNone(response.context['organization_list'])
        self.assertEqual(len(response.context['organization_list']), 2)
        self.assertIsNotNone(response.context['tags'])

    def test_index_view_tag_without_orgs(self):
        response = self.client.get('/orgs/tags/tagwithoutorg/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Security-Policy', response)
        self.assertCacheHeaders(response)
        self.assertIsNotNone(response.context['organization_list'])
        self.assertEqual(len(response.context['organization_list']), 0)
        self.assertIsNotNone(response.context['tags'])
        self.assertIn('Zur Zeit sind keine Gruppen vorhanden.', response.content)

    def test_index_view_tag_of_nonexisting_tag(self):
        response = self.client.get('/orgs/tags/nonexistingtag/')
        self.assertEqual(response.status_code, 404)
