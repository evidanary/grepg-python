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
    -v, --verbose                           Show debugging info
    -o, --global                            Search all public data on GrepPage
"""

import argparse

from sys import version_info as py_ver
from . import __version__ as version
from grepg import GrepG


USER_AGENT = 'grepg/{} (python {})'.format(version, '{}.{}.{}'.format(py_ver.major, py_ver.minor, py_ver.micro))
PROG = 'grepg'
DEFAULT_SUBCOMMAND = "search"

def create_parser():
    parser = argparse.ArgumentParser(prog=PROG)
    parser.add_argument('--verbose',
            action='store_true',
            help='Show debugging info')

    sub_parsers = parser.add_subparsers(dest='subcommand',
            help='sub-command help')

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

    # Show
    parser_show = sub_parsers.add_parser('show',
            help='Displays a resource on GrepPage')

    # Search
    parser_search = sub_parsers.add_parser('search',
            help='Searches for keywords')

    parser_search.add_argument('--global',
            action='store_true',
            help='Search all public data on GrepPage')
    parser_search.add_argument('keywords',
            nargs=argparse.REMAINDER)
    return parser

def get_args(args):
    if args[0].lower() not in "create configure show search".split():
        args.insert(0, DEFAULT_SUBCOMMAND)
    return args

def main():
    parser = create_parser()
    parsed_args = parser.parse_args(get_args(sys.argv[1:]))
    GrepG.create_command_clazz(parsed_args).execute()

if __name__ == '__main__':
    import sys
    sys.exit(main())
