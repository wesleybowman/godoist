"""
An example of how to use the GitHub GraphQL API
"""
from typing import Any, Dict

import requests
from pathlib import Path

from config import config

HEADERS = {"Authorization": f"Bearer {config['GITHUB_PERSONAL_ACCESS_TOKEN']}"}


def run_query(query: str, variables: Dict[str, str]) -> Dict[str, Any]:
    """
    A simple function to use requests.post to make the API call. Note the json= section.
    """

    json_data = {'query': query, 'variables': variables}
    request = requests.post('https://api.github.com/graphql',
                            json=json_data,
                            headers=HEADERS)

    if request.status_code == 200:
        return request.json()

    else:
        raise Exception(f'Query failed to run by returning code of {request.status_code}. {query}')


# Load in the search mentons query
gql_file = Path('./scripts/graphql_queries/search_mentions_query.gql')
with gql_file.open('r', encoding='utf-8') as f:
    search_mentions_query = ''.join(f.readlines())


# Variables used in the query that will change.
organization = 'wesleybowman'
repository = 'godoist'
# Testing on more than this repo (it works!)
# organization = 'channable'
# repository = 'requestmachine'
repo_string = f'repo:{organization}/{repository}'
user_name = 'wesleybowman'
mentions = f'mentions:{user_name}'

# Date format(missing UTC offset at the end): YYYY-MM-DDTHH:MM:SS
last_date_checked = '2018-11-02'
updated = f'updated:>={last_date_checked}'

variables = {
  'query_string': f'{repo_string} {mentions} {updated} sort:updated-desc'
}

# Execute the query
result = run_query(search_mentions_query, variables)
print(f'Result: {result}')

# Now that I have the result, I need to parse it.
# Mentions specifically need quite a bit of parsing I think, since the search doesn't return
# comments specifically, but instead Issues and PRs, which I will then need to go over all the 
# comments and filter out the dates that aren't >= `last_date_checked`. My idea right now is to 
# keep track of the last updated date, in a file or DB somewhere. And then update that once we've
# created the tasks in Todoist.
