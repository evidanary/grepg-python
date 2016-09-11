from __future__ import print_function

import logging
import json
import urllib2


LOG = logging.getLogger(__name__)
#BASE_URL = 'https://www.greppage.com/api'
BASE_URL = 'http://127.0.0.1:4567/api'
GUEST_ACCESS_TOKEN = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImFsZyI6IkhTMjU2IiwidHlwIjoiSldUIn0.eyJpZCI6MjAwMDAwMDAwMCwiZW1haWwiOiJndWVzdEBndWVzdC5jb20iLCJuYW1lIjoiZ3Vlc3QiLCJleHAiOjE1MTExMzY4MzB9.gWohR7LLtROgjSl5SxbEaGRBveZQEv7Uj2rzmgYrbys'


# Gets the json object from the URL
def get(endpoint):
    try:
        request = urllib2.Request(BASE_URL + endpoint)
        request.add_header('Authorization', GUEST_ACCESS_TOKEN)
        # print("Get {0}".format(endpoint))
        json_response = urllib2.urlopen(request).read()
        # print("Fetched resp {0}".format(json_response))
        return json.loads(json_response)
    except (urllib2.HTTPError, urllib2.URLError) as e:
        raise e
