from config import config
from app.todoist.core import Todoist


def requested_reviews_to_todoist():
    todoist = Todoist(config['TODOIST_API_TOKEN'])
    todoist.add_github_requested_reviews()

if __name__ == "__main__":
    requested_reviews_to_todoist()
