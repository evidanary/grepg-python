from __future__ import print_function
from grepg.command import Command
from grepg.model import Item
from grepg.util import *

class Search(Command):
    def __init__(self, parsed_args):
        self.parsed_args = parsed_args
        self.colorize = parsed_args.colorize

    def execute(self):
        endpoint = '/search?wt=json&q={0}'.format('%20'.join(self.parsed_args.keywords))
        endpoint = '%20'.join([endpoint, '%20AND%20type:cheat'])
        search_results = get(endpoint)

        for item in search_results['docs']:
            if(item['type'] == 'cheat'):
                print_util(item['description'], 'blue', self.colorize)
                print(item['command'], "\n")

        if not len(search_results['docs']) > 0 :
            print('No items found for "{0}"'.format(" ".join(self.parsed_args.keywords)))
