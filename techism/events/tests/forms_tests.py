#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase
from techism.events.forms import EventForm, CommaSeparatedTagsFormField
from techism.models import EventTag
from django.core.exceptions import ValidationError

class EventFormsTest(TestCase):
    
    fixtures = ['test-utils/fixture.json']
    
    def test_comma_separated_tags_form_field_is_required(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        try:
            field.clean("")
            self.fail("Must throw ValidationError")
        except ValidationError:
            pass
        
    def test_comma_separated_tags_form_field_existing_tags(self):
        python = EventTag.objects.get(name="python")
        java = EventTag.objects.get(name="java")
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        tags = field.clean("python, java")
        self.assertItemsEqual((python,java), tags)
        self.assertEqual(5, EventTag.objects.count())
        
    def test_comma_separated_tags_form_field_new_tags(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        tags = field.clean("foo, bar")
        self.assertEqual(2, len(tags))
        self.assertEqual(tags[0], EventTag.objects.get(name="foo"))
        self.assertEqual(tags[1], EventTag.objects.get(name="bar"))
        self.assertEqual(7, EventTag.objects.count())
        
    def test_comma_separated_tags_form_field_strip_lowercase_filter_empty_and_duplicates(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        tags = field.clean("foo, , Foo Bar,, bar, FOO ,")
        self.assertEqual(3, len(tags))
        self.assertEqual(tags[0], EventTag.objects.get(name="foo"))
        self.assertEqual(tags[1], EventTag.objects.get(name="foo bar"))
        self.assertEqual(tags[2], EventTag.objects.get(name="bar"))
        self.assertEqual(8, EventTag.objects.count())

    def test_comma_separated_tags_form_field_allowed_characters(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        tags = field.clean("foo, a_z-0.9 äöüß")
        self.assertEqual(2, len(tags))
        self.assertEqual(tags[0], EventTag.objects.get(name="foo"))
        self.assertEqual(tags[1], EventTag.objects.get(name="a_z-0.9 äöüß"))
        self.assertEqual(7, EventTag.objects.count())

    def test_comma_separated_tags_form_field_not_allowed_characters(self):
        field = CommaSeparatedTagsFormField(max_length=200, label= u'Tags', required=True)
        try:
            field.clean("foo, <script>")
            self.fail("Must throw ValidationError")
        except ValidationError:
            pass