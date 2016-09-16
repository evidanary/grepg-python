from __future__ import print_function
from grepg.command import Command
from grepg.model import Item
from grepg.util import *

class Show(Command):
    def __init__(self, parsed_args):
        self.topic = parsed_args.topic_name[0]
        self.colorize = not parsed_args.no_colorize


    # TODO: THis should work similar to
    # the original grepg client
    def execute(self):
        exit_if_no_auth()
        available_topics = get_user_topics()
        matched_topics = filter(lambda topic_obj: starts_with_case_insensitive(self.topic, topic_obj.name),  available_topics)

        if matched_topics:
            topic_id = matched_topics[0].id
            items = get(cheats_uri(topic_id))
            for item in items:
                print_util(item['description'], 'blue', self.colorize)
                print(item['command'], "\n")
        else:
            raise ValueError('Could not find topic {0}. Available Topic Names: {1}'.format(self.topic,
                ",".join([topic.name for topic in available_topics])))
