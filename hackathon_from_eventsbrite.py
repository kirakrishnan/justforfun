"""
extracts all the events in DC, MD, VA and checks for events which are hackathon
and prints the hackathon events
"""

import requests
import json
import os
import pprint
from secret_settings import eventbrite_api_key

api_key = eventbrite_api_key
url = 'https://www.eventbriteapi.com/v3/events/search'

headers = {
    "Authorization": "Bearer {0}".format(api_key),
    "content-type": "application/json"
}

# search for events with these parameters
search_dc = {
    "address": "district of columbia",
    "within": "15mi"
}

search_va = {
    "address": "virginia",
    "within": "15mi"
}

search_md = {
    "address": "maryland",
    "within": "15mi"
}


def get_events(params):
    """
    Takes headers and params as input and returns the list of events in current page
    """
    req = requests.get("https://www.eventbriteapi.com/v3/events/search", headers=headers, params=params)
    events = json.loads(req.content)['events']
    return events


def get_pagination(params):
    """
    Takes headers and params as input and returns the pagination details for the current request
    """
    req = requests.get("https://www.eventbriteapi.com/v3/events/search", headers=headers, params=params)
    pagination = json.loads(req.content)['pagination']
    return pagination['page_count']


def get_hackathon(state, distance, last_page):
    """
    runs thru each page and extracts all the events in tha page and filters the events which have hacathon in
    either title or decription
    :param state:
    :param distance:
    :param last_page:
    :return:
    """
    for page in range(1,last_page):
        params = {
            "location.address": state,
            "location.within": distance,
            "page": page
        }
        events = get_events(params)
        # pprint.pprint(events)
        for event in events:
            result = {}
            name = event.get('name', '')
            description = event.get('description', '')
            if (name):
                text = name.get('text', '')
                text_desc = name.get('text', '')
                if ("hackathon" in text.lower() or "hackathon" in text_desc):
                    result['title'] = text
                    result['url'] = url
                    pprint.pprint(result)


def process_events(search):
    state = search['address']
    distance = search['within']
    params = {
        "location.address": state,
        "location.within": distance,
        "page": 1
    }
    pagination_details = get_pagination(params)
    get_hackathon(state, distance, pagination_details)
    return

process_events(search_dc)
process_events(search_md)
process_events(search_va)

# prompts you once the process is complete. comment it if you are not using mac
os.system("say hey kira! executed successfully please check the output file")
