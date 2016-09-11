from __future__ import print_function

from .subcommands.search import Search
from .subcommands.configure import Configure
from .subcommands.show import Show
from .subcommands.create import Create

class GrepG(object):
    @staticmethod
    def create_command_clazz(parsed_args):
        if(parsed_args.subcommand.lower() == 'search'):
            return Search(parsed_args)
        elif(parsed_args.subcommand.lower() == 'configure'):
            return Configure(parsed_args)
        elif(parsed_args.subcommand.lower() == 'show'):
            return Show(parsed_args)
        elif(parsed_args.subcommand.lower() == 'create'):
            return Create(parsed_args)




