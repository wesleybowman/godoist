"""
An example of how to use the GitHub GraphQL API
"""
from typing import Any, Dict, Optional

import requests
from pathlib import Path

from config import config

HEADERS = {"Authorization": f"Bearer {config['GITHUB_PERSONAL_ACCESS_TOKEN']}"}


def run_query(query: str) -> Dict[str, Any]:
    """
    A simple function to use requests.post to make the API call. Note the json= section.
    """

    json_data = {'query': query}
    request = requests.post('https://api.github.com/graphql',
                            json=json_data,
                            headers=HEADERS)

    if request.status_code == 200:
        return request.json()

    else:
        raise Exception(f'Query failed to run by returning code of {request.status_code}. {query}')


def load_query(query_filepath):
    """
    Load a gql file
    """

    gql_file = Path(query_filepath)
    with gql_file.open('r', encoding='utf-8') as f:
        gql_query = ''.join(f.readlines())

    return gql_query


def main():

    query_filepath = './scripts/graphql_queries/mentions.gql'
    mentions_query = load_query(query_filepath)

    query_filepath = './scripts/graphql_queries/review_requested.gql'
    review_requested_query = load_query(query_filepath)

    gql_query = f'{{{mentions_query}{review_requested_query}}}'


    # Execute the query
    result = run_query(gql_query)
    print(f'Result: {result}')

    return result


if __name__ == '__main__':
    result = main()
