from __future__ import print_function

import logging
import os
import json
import yaml
import urllib2


LOG = logging.getLogger(__name__)
#BASE_URL = 'https://www.greppage.com/api'
BASE_URL = 'http://127.0.0.1:4567/api'
GUEST_ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIn0.eyJpZCI6MjAwMDAwMDAwMCwiZW1haWwiOiJndWVzdEBndWVzdC5jb20iLCJuYW1lIjoiZ3Vlc3QiLCJleHAiOjE1MTExMzY4MzB9.gWohR7LLtROgjSl5SxbEaGRBveZQEv7Uj2rzmgYrbys'
WRITE_TO_CREDS_FILE = ['secret_access_key']

# Gets the json object from the URL
def get(endpoint):
    try:
        request = urllib2.Request(BASE_URL + endpoint)
        request.add_header('Authorization', 'Bearer ' +
                get_settings('secret_access_key', GUEST_ACCESS_TOKEN))
        json_response = urllib2.urlopen(request).read()
        return json.loads(json_response)
    except (urllib2.HTTPError, urllib2.URLError) as e:
        raise e


def post(endpoint, data):
    try:
        #data = urllib2.urlencode(data)
        data = json.dumps(data, ensure_ascii=False)
        request = urllib2.Request(BASE_URL + endpoint, data)
        request.add_header('Authorization', 'Bearer ' +
                get_settings('secret_access_key', GUEST_ACCESS_TOKEN))
        json_response = urllib2.urlopen(request).read()
        return json.loads(json_response)
    except (urllib2.HTTPError, urllib2.URLError) as e:
        raise e

def user_dir():
      return os.path.expanduser("~")

def get_settings(key_name, default=None):
    file_to_load = 'credentials.yml' if(key_name in WRITE_TO_CREDS_FILE) else 'settings.yml'
    home = user_dir()
    user_settings_file = os.path.join(home,
                '.grepg', file_to_load)
    if os.path.exists(user_settings_file):
        with open(user_settings_file) as user_config_file:
            try:
                yaml_dict = yaml.load(user_config_file)
                if key_name in yaml_dict:
                    return yaml_dict[key_name]
            except Exception as e:
                raise e
        return default

def create_item_on_remote(item):
    user_name = get_settings('user_name')
    data = [{"command": item.command,
            "description": item.description}]
    endpoint = '/users/{0}/sheets/{1}/cheats'.format(user_name, item.topic_id)
    post(endpoint, data)
