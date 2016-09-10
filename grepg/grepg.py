from __future__ import print_function

from .subcommands.search import Search

class GrepG(object):
    @staticmethod
    def create_command_clazz(parsed_args):
        if(parsed_args.subcommand == 'search'):
            return Search(parsed_args)




