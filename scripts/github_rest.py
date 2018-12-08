import requests

from config import config

base_url = 'https://api.github.com'
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    "Authorization": f"Bearer {config['GITHUB_PERSONAL_ACCESS_TOKEN']}",
    }


# Repo specific
# /repos/:owner/:repo/notifications
url = f'{base_url}/notifications'

# Only shows notifications in which the user is directly participating or mentioned
# Can also have a `since` parameter as well.
# url = f'{base_url}/notifications?participating=true'

params = {
    'particpating': True,
    # 'since': '2018-12-07',
    'page': 2
}

response = requests.get(url, headers=HEADERS, params=params)
resp_json = response.json()

# For pagination, I think we have to use to `Link` in headers
# response.headers['Link']
# response:
# '<https://api.github.com/notifications?particpating=True&page=2>; rel="next", 
#  <https://api.github.com/notifications?particpating=True&page=2>; rel="last"'
#
# We can parse the above to get the last page and then iterate over.
