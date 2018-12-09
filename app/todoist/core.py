import json
import requests
import uuid
from typing import Dict

from config import config


class Todoist:

    def __init__(self, todoist_api_token):

        self.headers = {
            'Authorization': f'Bearer {todoist_api_token}',
            'Content-Type': 'application/json',
            # What is `X-Request-Id`: https://stackoverflow.com/a/27174552/1141389
            'X-Request-Id': str(uuid.uuid4()),
        }

    def get(self, url):
        """
        Returns both the response and the json from the request.
        """

        resp = requests.get(url, headers=self.headers)
        resp_json = resp.json()

        return resp, resp_json

    def post(self, url):
        """
        Returns both the response and the json from the request.
        """

        resp = requests.post(url, headers=self.headers)
        resp_json = resp.json()

        return resp, resp_json

    def get_project_name_to_id_lookup(self) -> Dict[str, int]:
        """
        Get the lookup that maps the project name to the project id.
        """

        url = 'https://beta.todoist.com/API/v8/projects'

        _, projects = self.get(url)

        project_name_to_id_lookup: Dict[str, int] = {
            project['name']: project['id'] 
            for project in projects
        }

        return project_name_to_id_lookup