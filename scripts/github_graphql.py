"""
An example of how to use the GitHub GraphQL API
"""
import requests
from pathlib import Path

from config import config

HEADERS = {"Authorization": f"Bearer {config['GITHUB_PERSONAL_ACCESS_TOKEN']}"}


def run_query(query):
    """
    A simple function to use requests.post to make the API call. Note the json= section.
    """
    request = requests.post('https://api.github.com/graphql',
                            json={'query': query},
                            headers=HEADERS)

    if request.status_code == 200:
        return request.json()

    else:
        raise Exception(f'Query failed to run by returning code of {request.status_code}. {query}')


# Load in the search mentons query
gql_file = Path('./scripts/graphql_queries/search_mentions_query.gql')
with gql_file.open('r', encoding='utf-8') as f:
    search_mentions_query = ''.join(f.readlines())

# Execute the query
result = run_query(search_mentions_query)
print(f'Result: {result}')
