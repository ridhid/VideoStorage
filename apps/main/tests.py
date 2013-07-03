"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import Client


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class CommonTest(TestCase):

    client = Client()

    def test_main(self):
        url = reverse('main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, 'Беда на главной! Свистать всех на верх!')