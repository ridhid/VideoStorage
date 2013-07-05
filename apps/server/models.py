#coding: utf-8
from django.db import models

import ConfigParser
from camsViewer import settings

#todo модель с конфигами сервера
class Config(models.Model):

    configfile = settings.CAMS_SERVER_SETTINGS_FILE

    @property
    def config(self):
        if not hasattr(self, "_config"):
            self._config = ConfigParser.RawConfigParser()
        return self._config

    @config.setter
    def config(self, value):
        config = self.config
        config.read(value)

    def __init__(self, configfile=None):
        configfile = configfile or self.configfile
        self.config = configfile

    def to_dict(self):
        config = self.config
        def get_items(section):
            items = list()
            [items.append({'header': header, 'value': value}) for header, value
                in config.items(section)]
            return items
        return map(lambda section: dict(name=section, items=get_items(section)),
            config.sections())