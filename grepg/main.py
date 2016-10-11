#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys

from grepg import GrepG
from . import __version__

PROG = 'grepg'
DEFAULT_SUBCOMMAND = "search"

# Get parsed arguments from the commandline
def get_parsed_args():
    parser = argparse.ArgumentParser(prog=PROG)
    parser.add_argument('--debug',
            action='store_true',
            help='Show debugging info')
    parser.add_argument('--version',
            action='version',
            version='%(prog)s {version}'.format(version=__version__))

    sub_parsers = parser.add_subparsers(dest='subcommand',
            help='sub-command help')

    # Search
    parser_search = sub_parsers.add_parser('search',
            help='Searches for keywords')


    parser_search.add_argument('--no_colorize',
            action='store_true',
            help='Dont Colorize the output')
    parser_search.add_argument('-l', '--local_search',
            action='store_true',
            help='Search my data only')
    parser_search.add_argument('-n', '--no_pager',
            action='store_true',
            help='Dont use a pager (less) to display output')
    parser_search.add_argument('keywords',
            nargs=argparse.REMAINDER)

    # Configure
    parser_configure = sub_parsers.add_parser('configure',
            help='Configures the client for accessing private data')

    # Create
    parser_create = sub_parsers.add_parser('create',
            help='Creates a resource on GrepPage')
    create_sp = parser_create.add_subparsers(dest="create_subcommand",
            help="Create Command Help")
    create_item_parser = create_sp.add_parser('item',
            help="Create an item")
    create_topic_parser = create_sp.add_parser('topic',
            help="Create a topic")
    create_topic_parser.add_argument('topic_name',
            help="Create a topic with the name. Don't create if already exists")
    create_topic_parser.add_argument('-p', '--private',
            action='store_true',
            help='Create a private topic')

    # Show
    parser_show = sub_parsers.add_parser('show',
            help='Displays a resource on GrepPage')
    parser_show.add_argument('topic_name',
            nargs=1)
    parser_show.add_argument('--no_colorize',
            action='store_true',
            help='Dont Colorize the output')

    parsed_args = parser.parse_args(get_args(sys.argv[1:]))
    return parsed_args

# Gets arguments: The default subcomman is search
def get_args(args):
    if len(args) == 0:
        args.insert(0, '--help')
    elif args[0].lower() in ['-h', '--help', '-d', '--debug', '-v', '--version']:
        pass
    elif args[0].lower() not in "create configure show search".split():
        args.insert(0, DEFAULT_SUBCOMMAND)
    return args

def main():
    parsed_args = get_parsed_args()
    GrepG.create_command_clazz(parsed_args).execute()

# Shows stack trace only when debug
def exceptionHandler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    if get_parsed_args().debug:
        debug_hook(exception_type, exception, traceback)
    else:
        print("{0}: {1}".format(exception_type.__name__, exception))

sys.excepthook = exceptionHandler

if __name__ == '__main__':
    import sys
    sys.exit(main())
