"""
"manage.py test".

"""

from django.test import TestCase
from event_service import get_tags


class SimpleTest(TestCase):
    
    def test_tags(self):
        tags = get_tags()
        self.assertEqual(tags.count(), 0)
