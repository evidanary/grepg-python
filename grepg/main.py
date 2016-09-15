#!/usr/bin/env python
from __future__ import print_function

""" grepg - A command-line search utility for GrepPage (www.greppage.com)

Usage:
    grepg ruby file open # searches for "ruby file open"
    grepg

Query: Search Query keywords e.g. "ruby open file"
Sub-Command:
    configure         Configures the client for accessing private data
    create item       Open editor to add an item
    create topic      Adds a topic
    show topic        Shows all items in a topic
    search            Searches for keywords
Options:
    -h, --help                              Lists help
    -d, --debug                             Show debug info
    -v, --version                           Show version
    -o, --global                            Search all public data on GrepPage
"""

import argparse
import sys

from grepg import GrepG
from . import __version__

PROG = 'grepg'
DEFAULT_SUBCOMMAND = "search"

def create_parser():
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
    parser_search.add_argument('-g', '--global_search',
            action='store_true',
            help='Search all public data on GrepPage')
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

    return parser

def get_args(args):
    if len(args) == 0:
        args.insert(0, '--help')
    elif args[0].lower() in ['-h', '--help', '-d', '--debug', '-v', '--version']:
        pass
    elif args[0].lower() not in "create configure show search".split():
        args.insert(0, DEFAULT_SUBCOMMAND)
    return args

def main():
    parser = create_parser()
    parsed_args = parser.parse_args(get_args(sys.argv[1:]))
    GrepG.create_command_clazz(parsed_args).execute()

if __name__ == '__main__':
    import sys
    sys.exit(main())
