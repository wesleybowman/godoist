import re
import requests
from typing import List

from config import config

BASE_URL = 'https://api.github.com'
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    "Authorization": f"Bearer {config['GITHUB_PERSONAL_ACCESS_TOKEN']}",
    }


# Repo specific
# /repos/:owner/:repo/notifications
# url = f'{BASE_URL}/notifications'

# Only shows notifications in which the user is directly participating or mentioned
# Can also have a `since` parameter as well.
# url = f'{base_url}/notifications?participating=true'

# I like using a params dict better than just putting them into the URL manually. 
# I think it is more readable this way. However, using response.links, I get the entire URL, so
# if I wanted to continue using the params dict, I would need to do parsing all the time. 
# Could do one request with params dict, and then only if we have more pages, switch to using the
# full URL.
params = {
    'particpating': True,
    # 'since': '2018-12-07',
    # Max items per page (not all endpoints can use this)
    'per_page': 100
}

url = f'{BASE_URL}/notifications?participating=true&per_page=10'

has_more_pages = True

page_count = 0
total_pages = 0
total_response: List = []
while has_more_pages:

    page_count += 1
    if total_pages:
        print(f'On page {page_count} of {total_pages}')

    else:
        print(f'On page {page_count}')

    # response = requests.get(url, headers=HEADERS, params=params)
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    resp_json = response.json()
    total_response.extend(resp_json)

    next_link = response.links.get('next')
    last_link = response.links.get('last')

    # This is just here for reporting, especially while I test all the different things I can do.
    # We could use this to figure out how many pages we have, and then just do a loop over that 
    # instead of using a while loop. Not sure what is better. Feels like a while loop would be
    # more robust in the end
    if last_link:
        # I love regular expressions
        matches = re.findall(r'&page=(\d+)', last_link['url'])
        total_pages = matches[0]

    # Get the next url in the pagination.
    if next_link:
        url = next_link['url']

    # Stop the pagination
    else:
        has_more_pages = False
