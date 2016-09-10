from __future__ import print_function
from grepg.command import Command
from grepg.model import Item
from grepg.util import get

class Search(Command):
    def __init__(self, parsed_args):
        self.parsed_args = parsed_args

    def execute(self):
        endpoint = '/search?wt=json&q={0}'.format('%20'.join(self.parsed_args.keywords))
        endpoint = '%20'.join([endpoint, '%20AND%20type:cheat'])
        search_results = get(endpoint)

        for item in search_results['docs']:
            if(item['type'] == 'cheat'):
                display_item = Item(item['description'] ,  item['command'], item['id'])
            print(display_item)
            print('---------------------------------------')

        if not len(search_results['docs']) > 0 :
            print('None Found')

