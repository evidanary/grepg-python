from __future__ import print_function
from grepg.command import Command
from grepg.model import Item
from grepg.util import *
from urllib import urlencode

class Search(Command):
    def __init__(self, parsed_args):
        self.parsed_args = parsed_args
        self.scope = 'global' if parsed_args.global_search else 'local'
        self.colorize = not parsed_args.no_colorize

    def execute(self):
        encoded_params = urlencode({
                "scope": self.scope,
                "wt": "json",
                # we will only get the cheats and not topics
                "q": " ".join(self.parsed_args.keywords) + " AND type:cheat",
                })
        endpoint = '/search?{0}'.format(encoded_params)
        search_results = get(endpoint)

        for item in search_results['docs']:
            if(item['type'] == 'cheat'):
                print_util(item['description'], 'blue', self.colorize)
                print(item['command'], "\n")

        #Log the query
        log_query(" ".join(self.parsed_args.keywords), search_results["numFound"])

        if not len(search_results['docs']) > 0 :
            print('No items found for "{0}"'.format(" ".join(self.parsed_args.keywords)))
