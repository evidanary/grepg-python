from __future__ import print_function

import os
import yaml

from grepg.util import credentials_file, settings_file
from grepg.command import Command
from grepg.subcommands.writer import ConfigFileWriter

class Configure(Command):
    def __init__(self, parsed_args):
        self.parsed_args = parsed_args

    def read_config(self, filename):
        if os.path.exists(filename):
            with open(filename) as user_config_file:
                return yaml.load(user_config_file)
        return None

    # returns a new dict
    def merge_dicts(self, a, b):
        if a == None:
            return b.copy()
        z = a.copy()
        z.update(b)
        return z

    def execute(self):
        secrets, settings = {}, {}

        # Read from STDIN
        settings['user_name'] = raw_input('Default Username: ')
        secrets['secret_access_key'] = raw_input(
                'GrepPage Secret Access Key (Settings > Token > Secret API Key on greppage.com): ')

        # Merge configuration from what we already know
        credentials = self.merge_dicts(
                self.read_config(credentials_file()),
                secrets)
        settings = self.merge_dicts(
                self.read_config(settings_file()),
                settings)

        writer = ConfigFileWriter()
        writer.update_config(credentials,
                credentials_file())

        writer.update_config(settings,
                settings_file())

