from __future__ import print_function
from grepg.command import Command
from grepg.model import Item
from grepg.util import get

class Show(Command):
    def __init__(self, parsed_args):
        self.parsed_args = parsed_args


    # TODO: THis should work similar to
    # the original grepg client
    def execute(self):
        print('hi')

