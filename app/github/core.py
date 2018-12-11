
"""
An example of how to use the GitHub GraphQL API
"""
import json
from string import Template
from typing import Any, Dict, Optional

import requests
from pathlib import Path

from config import config

HEADERS = {"Authorization": f"Bearer {config['GITHUB_PERSONAL_ACCESS_TOKEN']}"}


def run_gql_query(query: str) -> Dict[str, Any]:
    """
    A simple function to use requests.post to make the API call.
    """

    json_data = {'query': query}
    request = requests.post('https://api.github.com/graphql',
                            json=json_data,
                            headers=HEADERS)

    # TODO: take care of when we get errors since errors return a 200 as well.
    if request.status_code == 200:
        return request.json()

    else:
        raise Exception(f'Query failed to run by returning code of {request.status_code}. {query}')


def load_gql_query(query_filepath):
    """
    Load a gql file.
    """

    gql_file = Path(query_filepath)
    with gql_file.open('r', encoding='utf-8') as f:
        gql_query = ''.join(f.readlines())

    return gql_query


def load_and_run_gql_query(query_filepath: str,
                           *,
                           variables: Optional[Dict[str, Any]] = None
                           ) -> Dict[str, Any]:
    """
    Load and run the GraphQL query.

    If `variables` are supplied, then replace the `key` of the `variables` dict with it's value.
    """

    query = load_gql_query(query_filepath)

    if variables:
        # Turn GraphQL string into a Template that we can fill
        template_query = Template(query)
        query = template_query.safe_substitute(variables)

    gql_query = f"""{{
        {query}
    }}"""

    # Execute the query
    result = run_gql_query(gql_query)
    return result


def get_mentions():
    """
    For now, only get the mentions, and with a hardcoded query to search for
    """

    query_filepath = './app/github/graphql/mentions.gql'

    result = load_and_run_gql_query(query_filepath)
    return result['data']['mentions']

def get_requested_reviews():
    """
    For now, only get the mentions, and with a hardcoded query to search for
    """

    user = 'wesleybowman'
    updated = '2017-12-07'
    query_string = f'type:pr state:open review-requested:{user} updated:>={updated}'
    # without json.dumps, this doesn't work. We could instead add `""` to the gql file, but that
    # is more confusing IMO
    variables = {
        'requested_reviews_query_string': json.dumps(query_string)
    }

    query_filepath = './app/github/graphql/requested_reviews.gql'

    result = load_and_run_gql_query(query_filepath, variables=variables)
    return result['data']['requested_reviews']


def get_mentions_and_requested_reviews():
    """
    Get my mentions and my requested reviews in one GraphQL query.

    For now, this is so I can be a little more efficient (or at least, I think more efficient, not
    100% sure that I understand GraphQL correctly) with my query. This is here until I can implement 
    a way to make composable GraphQL queries. I think I just need to have a way to store which 
    queries the user wants to run. Then I can compose them. That is a further down todo.
    """

    query_filepath = './app/github/graphql/mentions.gql'
    mentions_query = load_gql_query(query_filepath)

    query_filepath = './app/github/graphql/requested_reviews.gql'
    requested_reviews_query = load_gql_query(query_filepath)

    gql_query = f'{{{mentions_query}{requested_reviews_query}}}'

    result = run_gql_query(gql_query)
    return result
