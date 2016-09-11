from __future__ import print_function

import sys, tempfile, os
from subprocess import call
from grepg.command import Command
from grepg.model import Item
from grepg.util import get

class Create(Command):
    def __init__(self, parsed_args):
        self.parsed_args = parsed_args

    def create_item_template(self):
        template = '''topic:
description:
command:

# Please enter the relevant fields for the new item. Lines starting
# with '#' will be ignored, and empty fields will abort the create.
#
# Available topics: git, unix and ubuntu, markdown, scala
#
# Example New Item
# topic: git
# description: create a new branch
# command: git checkout -b NEW_BRANCH
'''
        return template

    def parse_item_from_input(self, contents):
        print('1')

    def create_item(self):
        EDITOR = os.environ.get('EDITOR','vim')
        # Write to file
        tf = tempfile.NamedTemporaryFile(suffix=".tmp")
        tf.write(self.create_item_template())
        tf.flush()

        call([EDITOR, tf.name])
        tf.flush()

        tf.seek(0)
        edited_message = tf.read()
        print(edited_message)

        #Parse contents from temp file
        #and create an Item
        self.parse_item_from_input(edited_message)

        #Create the item on remote server
        #create_item(item)

    def execute(self):
        if(self.parsed_args.create_subcommand.lower()
                == 'item'):
            self.create_item()
        elif(self.parsed_args.create_subcommand.lower()
                == 'topic'):
            print('yeay Create topic')


