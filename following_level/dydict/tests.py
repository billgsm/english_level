#-*- coding: utf-8 -*-
from django.test import TestCase


class SimpleTest(TestCase):
    def test_dydict(self):
        """
        check dydict views
        """
        self.assertEqual(1 + 1, 2)
