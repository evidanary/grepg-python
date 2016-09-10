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


def validate_args(parsed_args):
    pass

def main():
    # print(USER_AGENT)
    # print('GrepG command line client')

    parser = argparse.ArgumentParser(prog=PROG)
    parser.add_argument('--verbose', action='store_true', help='Show debugging info')

    sub_parsers = parser.add_subparsers(dest='subcommand', help='sub-command help')
    parser_configure = sub_parsers.add_parser('configure', help='Configures the client for accessing private data')
    parser_create = sub_parsers.add_parser('create', help='Creates a resource on GrepPage')
    parser_show = sub_parsers.add_parser('show', help='Displays a resource on GrepPage')
    parser_search = sub_parsers.add_parser('search', help='Searches for keywords')

    parser_search.add_argument('--global', action='store_true', help='Search all public data on GrepPage')
    parser_search.add_argument('keywords', nargs=argparse.REMAINDER)

    parsed_args = parser.parse_args(sys.argv[1:])
    validate_args(parsed_args)
    GrepG.create_command_clazz(parsed_args).execute()

if __name__ == '__main__':
    import sys
    sys.exit(main())
