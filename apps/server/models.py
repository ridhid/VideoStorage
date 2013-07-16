#coding: utf-8

import re
import commands
import ConfigParser
from camsViewer import settings


class Config(object):

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

    def save(self):
        with open(self.configfile, 'w') as cfg_file:
            self.config.write(cfg_file)

    def delete(self, section, option):
        if self.config.has_option(section, option):
            self.config.remove_option(section, option)
            self.save()

    def edit(self, section, option, value):
        if self.config.has_section(section):
            self.config.set(section, option, value)
            self.save()

    def to_dict(self):
        config = self.config
        def get_items(section):
            items = list()
            [items.append({'header': header, 'value': value}) for header, value
                in config.items(section)]
            return items
        return map(lambda section: dict(name=section, items=get_items(section)),
            config.sections())


class Command(object):
    """abstaract class for run specific command

    """
    cmd = None

    class ErroInCmd(Exception):
        def __repr__(self):
            return "Ошибка в выполнении команды"

    @property
    def value(self):
        status, output = commands.getstatusoutput(self.cmd)
        return self.process(output)

    def process(self, input):
        return input


class PatternMix(object):
    def process(self, input):
        match = re.search(self.pattern, input)
        if match:
            return {group: match.group(group) for group in self.output_groups}
        return {group: "" for group in self.output_groups}


class DfCommand(PatternMix, Command):
    cmd = r'df -h'
    pattern = r'(?P<dev>/dev/\w+)\s+(.+?)\s+(?P<usage>.+?)\s+(?P<available>.+?)\s+(?P<procent>.+?)%\s+/'
    output_groups = ('dev', 'usage', 'available', 'procent')


class Uptime(PatternMix, Command):
    cmd = "uptime"
    pattern = r'\s*(?P<time>..:..:..)\s+.*load average:\s+(?P<one>.*),\s+(?P<five>.*)\s(?P<fifteen>.*)'
    output_groups = ('time', 'one', 'five', 'fifteen')


class Status(PatternMix, Command):
    cmd = "./scripts/supervisorctl 'status video'"
    pattern = r'.*video.*?(?P<status>\w+).*pid\s+(?P<pid>\d+),.*?uptime.*?(?P<uptime>.*)'
    output_groups = ('status', 'pid', 'uptime')


class StopVideo(Command):
    cmd = r"./scripts/supervisorctl 'stop video'"


class StartVideo(Command):
    cmd = r"./scripts/supervisorctl 'start video'"