
mentions = {
    'query': """
        mentions: search(query: "{query_string}", type: ISSUE, first: 100) {{
            pageInfo {{
                hasNextPage
            }}
            edges {{
                node {{
                    __typename

                    ... on Issue {{
                        title
                        bodyText
                        updatedAt
                        comments(first: 100) {{
                            ...comment
                        }}
                    }}

                    ... on PullRequest {{
                        title
                        bodyText
                        updatedAt
                        comments(first: 100) {{
                            ...comment
                        }}
                    }}
                }}
            }}
        }}
    """,

    'fragments': """
        fragment comment on IssueCommentConnection {
            totalCount
            edges {
                node {
                    body
                    createdAt
                    updatedAt
                    url
                    author {
                        login
                    }
                }
            }
        }
    """

}

