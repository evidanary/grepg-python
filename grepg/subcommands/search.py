from __future__ import print_function
from grepg.command import Command
from grepg.model import Item
from grepg.util import *
from urllib import urlencode
from termcolor import colored, cprint

import pydoc
import sys

class Search(Command):
    # mixed scope shows a merge of user owned data and public data
    # local scope shows results on user owned data only
    DEFAULT_SEARCH_SCOPE = "mixed"
    ACTIVATE_PAGER_ITEM_COUNT = 5

    def __init__(self, parsed_args):
        self.parsed_args = parsed_args
        self.scope = 'local' if parsed_args.local_search else self.DEFAULT_SEARCH_SCOPE
        self.colorize = not parsed_args.no_colorize
        self.pager = not parsed_args.no_pager

    def raw_search_results(self):
        encoded_params = urlencode({
                "scope": self.scope,
                "wt": "json",
                # we will only get the cheats and not topics
                "q": " ".join(self.parsed_args.keywords) + " AND type:cheat",
                })
        endpoint = '/search?{0}'.format(encoded_params)
        return get(endpoint)

    def formatted_results(self, search_results_items):
        text = []
        for item in search_results_items:
            if(item['type'] == 'cheat'):
                if self.colorize:
                    text.append(" ".join([
                        colored(item['description'], 'blue'),
                        colored("[" + item['topic_name'] + "]", 'red', attrs=['bold']),
                        colored("(" + item["user_name"] + ")", "magenta")
                        ]))
                else:
                    text.append(" ".join([
                        item['description'],
                        "[" + item['topic_name'] + "]"
                        ]))
                text.append(item['command'] + "\n")
        return "\n".join(text)

    def print_results(self, text, result_items):
        cprint(text)
        if(self.pager and len(result_items) > self.ACTIVATE_PAGER_ITEM_COUNT):
            pydoc.pager(text)

    def execute(self):
        result = self.raw_search_results()
        result_items = result["docs"]
        final_text = self.formatted_results(result_items)
        self.print_results(final_text, result_items)

        #Log the query
        log_query(" ".join(self.parsed_args.keywords), result["numFound"])

        if not len(result_items) > 0 :
            print('No items found for "{0}". To search the web Cmd+Click this link https://google.com/search?q={0}'.format("+".join(self.parsed_args.keywords)))
