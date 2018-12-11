"""
An example of how to use the GitHub GraphQL API
"""
import json
from string import Template
from typing import Any, Dict, Iterator, NamedTuple, Optional

import requests
from pathlib import Path


class GithubRequestedReview(NamedTuple):
    """
    Structure always returned when you have a Requested Review

    TODO: Add more here (i.e. change the graphql query)
    """

    author: str
    title: str
    url: str
    updated_at: str


class Github:

    graphql_url = 'https://api.github.com/graphql'

    def __init__(self, github_personal_access_token):

        self.headers = {
            'Authorization': f'Bearer {github_personal_access_token}',
        }

    def run_gql_query(self, query: str) -> Dict[str, Any]:
        """
        A simple function to use requests.post to make the API call.
        """

        json_data = {'query': query}
        request = requests.post(self.graphql_url,
                                json=json_data,
                                headers=self.headers)

        # TODO: take care of when we get errors since errors return a 200 as well.
        if request.status_code == 200:
            return request.json()

        else:
            raise Exception(
                f'Query failed to run by returning code of {request.status_code}. {query}')

    @staticmethod
    def load_gql_query(query_filepath):
        """
        Load a gql file.
        """

        gql_file = Path(query_filepath)
        with gql_file.open('r', encoding='utf-8') as f:
            gql_query = ''.join(f.readlines())

        return gql_query

    def load_and_run_gql_query(self,
                               query_filepath: str,
                               *,
                               variables: Optional[Dict[str, Any]] = None
                               ) -> Dict[str, Any]:
        """
        Load and run the GraphQL query.

        If `variables` are supplied, then replace the `key` of the `variables` dict with it's value.
        """

        query = Github.load_gql_query(query_filepath)

        if variables:
            # Turn GraphQL string into a Template that we can fill
            template_query = Template(query)
            query = template_query.safe_substitute(variables)

        gql_query = f"""{{
            {query}
        }}"""

        # Execute the query
        result = self.run_gql_query(gql_query)
        return result

    def get_mentions(self):
        """
        For now, only get the mentions, and with a hardcoded query to search for
        """
        # TODO: get these from the parameters instead of being hardcoded.
        repo = 'wesleybowman/godoist'
        updated = '2018-12-02'
        query_string = f'repo:{repo} mentions:wesleybowman sort:updated-desc updated:>={updated}'

        variables = {
            'mentions_query_string': json.dumps(query_string)
        }

        query_filepath = './app/github/graphql/mentions.gql'

        result = self.load_and_run_gql_query(query_filepath, variables=variables)
        return result['data']['mentions']

    def get_requested_reviews(self):
        """
        For now, only get the mentions, and with a hardcoded query to search for
        """

        # TODO: get these from the parameters instead of being hardcoded.
        user = 'wesleybowman'
        updated = '2017-12-07'
        query_string = f'type:pr state:open review-requested:{user} updated:>={updated}'
        # without json.dumps, this doesn't work. We could instead add `""` to the gql file, but that
        # is more confusing IMO
        variables = {
            'requested_reviews_query_string': json.dumps(query_string)
        }

        query_filepath = './app/github/graphql/requested_reviews.gql'

        result = self.load_and_run_gql_query(query_filepath, variables=variables)
        return result['data']['requested_reviews']

    def get_mentions_and_requested_reviews(self):
        """
        Get my mentions and my requested reviews in one GraphQL query.

        For now, this is so I can be a little more efficient (or at least, I think more efficient,
        not 100% sure that I understand GraphQL correctly) with my query. This is here until I can
        implement a way to make composable GraphQL queries. I think I just need to have a way to
        store which queries the user wants to run. Then I can compose them.
        """

        # TODO: I think I can make the variables a property of the GitHub class, and then just use
        #  them as I need them
        # TODO: get these from the parameters instead of being hardcoded.
        user = 'wesleybowman'
        updated = '2017-12-07'
        rr_query_string = f'type:pr state:open review-requested:{user} updated:>={updated}'

        repo = 'wesleybowman/godoist'
        updated = '2018-12-02'
        m_query_string = f'repo:{repo} mentions:wesleybowman sort:updated-desc updated:>={updated}'

        variables = {
            'mentions_query_string': json.dumps(m_query_string),
            'requested_reviews_query_string': json.dumps(rr_query_string)
        }

        query_filepath = './app/github/graphql/mentions.gql'
        mentions_query = self.load_gql_query(query_filepath)

        query_filepath = './app/github/graphql/requested_reviews.gql'
        requested_reviews_query = self.load_gql_query(query_filepath)
        template = Template(requested_reviews_query)
        requested_reviews_query = template.safe_substitute(variables)

        gql_query = f"""{{
            {mentions_query}
            {requested_reviews_query}
        }}"""

        gql_query = Template(gql_query).safe_substitute(variables)

        result = self.run_gql_query(gql_query)
        return result

    @staticmethod
    def process_requested_reviews(requested_reviews: Dict[str, Any]
                                  ) -> Iterator[GithubRequestedReview]:
        """
        Process Requested Reviews

        From a normal request, `requested_reviews` is found here:
            requested_reviews = result['data']['requested_reviews']
        """
        # TODO: I could auto get the requested review here, but I think leaving it without allows
        #  this method to be more useful.

        for edge in requested_reviews['edges']:
            node = edge['node']

            requested_review = GithubRequestedReview(
                url=node['url'],
                title=node['title'],
                author=node['author']['login'],
                updated_at=node['updatedAt']
            )

            yield requested_review
