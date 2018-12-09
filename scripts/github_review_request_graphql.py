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


def load_query(query_filepath):
    """
    Load a gql file
    """

    gql_file = Path(query_filepath)
    with gql_file.open('r', encoding='utf-8') as f:
        gql_query = ''.join(f.readlines())

    return gql_query


def main():

    query_filepath = './scripts/graphql_queries/search_review_request_query.gql'
    gql_query = load_query(query_filepath)

    variables = {
      'query': 'type:pr state:open review-requested:wesleybowman updated:>=2018-12-07'
    }

    # Execute the query
    result = run_query(gql_query, variables)
    print(f'Result: {result}')


if __name__ == '__main__':
    main()
