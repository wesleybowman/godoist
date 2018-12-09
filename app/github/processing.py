from typing import Any, Dict, Iterator, NamedTuple

from app.github.core import get_mentions, get_mentions_and_requested_reviews, get_requested_reviews
from app.todoist.core import Todoist


class GithubRequestedReview(NamedTuple):
    """
    Structure always returned when you have a Requested Review

    TODO: Add more here (i.e. change the graphql query)
    """

    author: str
    title: str
    url: str
    updated_at: str




def process_mentions(mentions: Dict[str, Any]):
    """
    Process Mentions

    
    From a normal request, `mentions` is found here:
        requested_reviews = result['data']['mentions']
    """


def process_requested_reviews(requested_reviews: Dict[str, Any]) -> Iterator[GithubRequestedReview]:
    """
    Process Requested Reviews

    
    From a normal request, `requested_reviews` is found here:
        requested_reviews = result['data']['requested_reviews']
    """

    for edge in requested_reviews['edges']:
        node = edge['node']

        requested_review = GithubRequestedReview(
            url = node['url'],
            title = node['title'],
            author = node['author']['login'],
            updated_at = node['updatedAt']
        )

        yield requested_review

