from __future__ import print_function

import logging
import os
import json
import yaml
import urllib2

from sys import version_info as py_ver
from . import __version__ as version
from model import Topic
from termcolor import cprint
from datetime import datetime


LOG = logging.getLogger(__name__)
BASE_URL = 'https://www.greppage.com/api'
# BASE_URL = 'http://127.0.0.1:4567/api'
GUEST_ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIn0.eyJpZCI6MjAwMDAwMDAwMCwiZW1haWwiOiJndWVzdEBndWVzdC5jb20iLCJuYW1lIjoiZ3Vlc3QiLCJleHAiOjE1MTExMzY4MzB9.gWohR7LLtROgjSl5SxbEaGRBveZQEv7Uj2rzmgYrbys'
# Any variables specified in this list will be written to
# the ~/.aws/credentials file instead of ~/.aws/config.
WRITE_TO_CREDS_FILE = ['secret_access_key']
USER_AGENT = 'grepg/{} (python {})'.format(version, '{}.{}.{}'.format(py_ver.major, py_ver.minor, py_ver.micro))

# Gets the json object from the URL
def get(endpoint):
    try:
        request = urllib2.Request(BASE_URL + endpoint)
        request.add_header('Authorization', 'Bearer ' +
                get_settings('secret_access_key', GUEST_ACCESS_TOKEN))
        request.add_header('User-Agent', USER_AGENT)
        json_response = urllib2.urlopen(request).read()
        return json.loads(json_response)
    except Exception as e:
        raise Exception ("Server Error. {0}\nPlease write to support@greppage.com if you continue seeing this".format(e))

def sheets_uri():
    url = ('/').join(['/users', get_settings("user_name"), 'sheets_with_stats'])
    return url

def credentials_file():
    return os.path.join(user_dir(),
                '.grepg', 'credentials.yml')

def settings_file():
    return os.path.join(user_dir(),
                '.grepg', 'settings.yml')

def get_user_topics():
    topics = get(sheets_uri())
    topic_objects = []

    for topic in topics:
        topic_objects.append(
                Topic(topic["id"], topic["name"]))

    return topic_objects


def post(endpoint, data):
    try:
        data = json.dumps(data, ensure_ascii=False)
        request = urllib2.Request(BASE_URL + endpoint, data)
        request.add_header('Authorization', 'Bearer ' +
                get_settings('secret_access_key', GUEST_ACCESS_TOKEN))
        request.add_header('User-Agent', USER_AGENT)
        json_response = urllib2.urlopen(request).read()
        return json.loads(json_response)
    except (urllib2.HTTPError, urllib2.URLError) as e:
        raise Exception ("Server Error. {0}\nPlease write to support@greppage.com if you continue seeing this".format(e))

def user_dir():
      return os.path.expanduser("~")

def cheats_uri(topic_id):
        return ('/').join(['/users', get_settings('user_name'), 'sheets', str(topic_id), 'cheats'])

def get_settings(key_name, default=''):
    file_to_load = credentials_file() if(key_name in WRITE_TO_CREDS_FILE) else settings_file()
    if os.path.exists(file_to_load):
        with open(file_to_load) as user_config_file:
            try:
                yaml_dict = yaml.load(user_config_file)
                if key_name in yaml_dict and len(yaml_dict[key_name].strip()) > 0:
                    return yaml_dict[key_name]
            except Exception as e:
                raise e
    return default

def exit_if_no_auth():
    if len(get_settings('user_name').strip()) == 0 or len(get_settings('secret_access_key')) == 0:
        print('Missing user_name or secret_access_key.\n\nTo fix: Run grepg configure')
        # TODO : We need to handle this with an exception that will deal with exiting
        exit(1)

def create_item_on_remote(item):
    user_name = get_settings('user_name')
    data = [{"command": item.command,
            "description": item.description}]
    endpoint = '/users/{0}/sheets/{1}/cheats'.format(user_name, item.topic_id)
    post(endpoint, data)

def create_topic_on_remote(topic, is_private):
    user_name = get_settings('user_name')
    data = {"name": topic,
            "is_private": is_private}
    endpoint = '/users/{0}/sheets'.format(user_name)
    post(endpoint, data)

def starts_with_case_insensitive(prefix, string):
    return string.lower().startswith(prefix.lower())


def create_file(config_filename):
    # Create the file as well as the parent dir if needed.
    dirname = os.path.split(config_filename)[0]
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    with os.fdopen(os.open(config_filename,
            os.O_WRONLY | os.O_CREAT, 0o600), 'w'):
        pass

def log_query(search_str, count):
    log_file_name = os.path.join(user_dir(), '.grepg', 'queries.log')
    if not os.path.isfile(log_file_name):
        create_file(log_file_name)
    current_date_iso = datetime.utcnow().isoformat() + 'Z'
    with open(log_file_name, 'a') as fp:
        fp.write("{0}\t{1}\t{2}\n".format(current_date_iso, search_str, count))

def print_util(string, color, colorize):
  if colorize:
    cprint(string, color)
  else:
    print(string)
