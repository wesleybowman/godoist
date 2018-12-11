# GraphQL file conventions

Right now, each `gql` file only contains a the fields which we want to query. We do not include the
`query` itself, nor do we keep the leading and tailing `{}`

Example:

Instead of writing:
```
query {
    requested_reviews: search(query: $requested_reviews_query_string, type: ISSUE, first: 100) {
        issueCount
        pageInfo {
            endCursor
            startCursor
        }
        edges {
            node {
                ... on PullRequest {
                    repository {
                        nameWithOwner
                    }
                    number
                    url
                    author {
                        login
                    }
                    title
                    updatedAt
                }
            }
        }
    }
}
```

we would instead do

```
requested_reviews: search(query: $requested_reviews_query_string, type: ISSUE, first: 100) {
    issueCount
    pageInfo {
        endCursor
        startCursor
    }
    edges {
        node {
            ... on PullRequest {
                repository {
                    nameWithOwner
                }
                number
                url
                author {
                    login
                }
                title
                updatedAt
            }
        }
    }
}
```

This allows us to take multiple gql files and compose them together to make a larger single query.