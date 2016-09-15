from __future__ import print_function

import sys, tempfile, os
from subprocess import call
from grepg.command import Command
from grepg.model import Item
from grepg.util import *

class Create(Command):
    def __init__(self, parsed_args):
        self.parsed_args = parsed_args

    def comment_begin_string(self):
        return "###############  ADD ITEM TO GREPPAGE  ####################"

    def create_item_template(self):
        template = '''topic:
description:
command:

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

    def available_topics(self, join_str = ",\n"):
       self.topics = get_user_topics()
       return join_str.join([ str(topic) for topic in self.topics])

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
        if not (len(topic) > 0 and len(description) > 0 and len(command) > 0):
            raise Exception("Missing topic, description or command")
        matched_topics = filter(lambda topic_obj: starts_with_case_insensitive(topic,
            topic_obj.name), self.topics)

        if matched_topics:
            return Item(description, command, matched_topics[0].id)
        else:
            raise Exception("Could not find topic {0}. Available Topic Names: {1}".format(topic, self.available_topics(", ")))

    def create_item(self):
        template = self.create_item_template()
        edited_message = self.read_input_from_editor(template)
        #edited_message = template
        item = self.parse_item_from_user_input(edited_message)
        create_item_on_remote(item)
        print('Successfully created item')

    def create_topic(self):
        input_topic = self.parsed_args.topic_name
        is_private = self.parsed_args.private
        matched_topics = filter(lambda topic_obj: input_topic.lower() ==  topic_obj.name.lower(), get_user_topics())
        if len(matched_topics) > 0:
            print("Topic already exists: {0}".format(matched_topics[0]))
            exit(1)
        create_topic_on_remote(input_topic, is_private)
        print('Successfully created topic {0}'.format(input_topic))

    def execute(self):
        exit_if_no_auth()
        if(self.parsed_args.create_subcommand.lower()
                == 'item'):
            self.create_item()
        elif(self.parsed_args.create_subcommand.lower()
                == 'topic'):
            self.create_topic()


