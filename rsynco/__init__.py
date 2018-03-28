from configobj import ConfigObj
from validate import Validator
import queue

job_queue = queue.Queue()


class Config:
    config_file = ''
    config_spec = ''

    def __init__(self, config_file=None, config_spec=None):
        if config_file is not None:
            type(self).config_file = config_file

        if config_spec is not None:
            type(self).config_spec = config_spec

        self.data = ConfigObj(type(self).config_file, configspec=type(self).config_spec)
        validator = Validator()

        if not self.data.validate(validator):
            self.data = None

    def update(self):
        self.data.write()

    def refresh(self):
        self.data.reload()

    def add_section(self, section_name):
        self.data[section_name] = {}
