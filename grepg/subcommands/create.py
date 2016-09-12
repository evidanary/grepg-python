from __future__ import print_function

import sys, tempfile, os
from subprocess import call
from grepg.command import Command
from grepg.model import Item
from grepg.util import get, create_item_on_remote, get_user_topics, starts_with_case_insensitive

class Create(Command):
    def __init__(self, parsed_args):
        self.parsed_args = parsed_args

    def comment_begin_string(self):
        return "###############  ADD ITEM TO GREPPAGE  ####################"

    def create_item_template(self):
        template = '''topic: abc
description: abc
command: abc

{comment}
(Anything below this line will be ignored)

Available topics: {available_topics}

Example
topic: git
description: create a new branch
command: git checkout -b NEW_BRANCH
'''.format(comment=self.comment_begin_string(),
        available_topics=self.available_topics())
        return template

    def available_topics(self):
       self.topics = get_user_topics()
       return ','.join([ str(topic) for topic in self.topics])

    def read_input_from_editor(self, start_content):
        EDITOR = os.environ.get('EDITOR','vim')
        # Write to file
        tf = tempfile.NamedTemporaryFile(suffix=".tmp",
                delete=False)
        tf.write(start_content)
        tf.flush()
        tf.close()

        call([EDITOR, tf.name])

        with open(tf.name) as g:
            contents = g.read()
        os.remove(tf.name)
        return contents

    def index_of_first_occurence(self, start, lines):
        return [ i for i, word in enumerate(lines) if word.startswith(start) ][0]

    def extract_field(self, field, lines):
        lines[0] = lines[0].replace(field,"")
        return "\n".join(lines)

    def parse_item_from_user_input(self, text):
        lines = text.split("\n")
        topic_line_index = self.index_of_first_occurence('topic:', lines)
        description_line_index = self.index_of_first_occurence('description:', lines)
        command_line_index = self.index_of_first_occurence('command:', lines)
        comment_line_index = self.index_of_first_occurence(self.comment_begin_string(), lines)

        topic = self.extract_field('topic:',
                lines[topic_line_index:description_line_index]).strip()
        description = self.extract_field('description:',
                lines[description_line_index:command_line_index]).strip()
        command = self.extract_field('command:',
                lines[command_line_index:comment_line_index]).strip()
        print('topic: {0}, description: {1}, command: {2}'.format(topic_line_index,
            description_line_index, command_line_index))
        print('Topic: {0}'.format(topic))
        print('Des: {0}'.format(description))
        print('comm: {0}'.format(command))

        # we need to get topic_id from cache
        matched_topics = filter(lambda topic_obj: starts_with_case_insensitive(topic, topic_obj.name),  self.topics)

        if matched_topics:
            return Item(description, command, matched_topics[0].id)
        else:
            raise Exception('Could not find topic {0}. Available Topic Names: {1}'.format(topic, self.available_topics()))

    def create_item(self):
        template = self.create_item_template()
        edited_message = self.read_input_from_editor(template)
        #edited_message = template
        item = self.parse_item_from_user_input(edited_message)

        create_item_on_remote(item)

    def execute(self):
        if(self.parsed_args.create_subcommand.lower()
                == 'item'):
            self.create_item()
        elif(self.parsed_args.create_subcommand.lower()
                == 'topic'):
            print('yeay Create topic')


