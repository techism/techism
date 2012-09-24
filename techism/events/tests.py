"""
"manage.py test".

"""

from django.test import TestCase
from event_service import get_current_tags


class SimpleTest(TestCase):
    
    fixtures = ['fixture.json']
    
    def test_tags(self):
        it = get_current_tags()
        tag1 = it.next()
        self.assertEqual("java", tag1.name)
        self.assertEqual(1, tag1.num_tags)
        tag2 = it.next()
        self.assertEqual("python", tag2.name)
        self.assertEqual(1, tag2.num_tags)
        tag3 = it.next()
        self.assertEqual("test", tag3.name)
        self.assertEqual(2, tag3.num_tags)
        with self.assertRaises(StopIteration): 
            it.next()
