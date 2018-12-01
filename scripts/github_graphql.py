"""
An example of how to use the GitHub GraphQL API
"""
import requests

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

        
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
query = """
query {
  search(query:  "repo:wesleybowman/godoist author:wesleybowman", type: ISSUE, first: 10) {
    repositoryCount
    edges {
      node {
        ... on Issue {
          bodyText
          title
          updatedAt
        }
      }
    }
  }
}
"""

# Execute the query
result = run_query(query)
print(f'Result: {result}')
