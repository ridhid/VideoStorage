#coding: utf-8


from json import dumps
from ConfigParser import RawConfigParser
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from apps.server.models import Config


class TestConfigCreater(object):
    filename = "config.test"

    section = 'MAIN'

    options = (
        ('header', 'value'),
        ('header2', 'value2'),
        ('header3', 'value3'),
    )

    def __init__(self):
        self.config = RawConfigParser()
        self.config.read(self.filename)

        if not self.config.has_section(self.section):
            self.config.add_section(self.section)

        for option in self.options:
            header, value = option
            self.config.set(self.section, header, value)

        with open(self.filename, 'w') as f:
            self.config.write(f)


class TestConfigModel(TestCase):
    filename = "config.test"

    std_config = [
        {
            'name': 'MAIN',
            'items': [
                dict(header='header', value='value'),
                dict(header='header2', value='value2'),
                dict(header='header3', value='value3'),
            ]
        }
    ]

    def setUp(self):
        TestConfigCreater()
        self.config = Config(self.filename)

    def test_to_dict(self):
        out = self.config.to_dict()
        self.assertEqual(out, self.std_config)


class TestConfigView(TestCase):

    client = Client()

    def setUp(self):
        TestConfigCreater()

    def test_config_view(self):
        url = reverse('config')
        response = self.client.get(url)
        expected_data = dumps(TestConfigModel.std_config)
        print response.content, expected_data
        self.assertJSONEqual(response.content, expected_data)