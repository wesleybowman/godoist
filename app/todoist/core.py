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

        # Todoist API urls
        # TODO: make a `self.urls` lookup instead? 
        self.projects_url = 'https://beta.todoist.com/API/v8/projects'
        self.tasks_url = 'https://beta.todoist.com/API/v8/tasks'


    def get(self, url):
        """
        Returns both the response and the json from the request.
        """

        resp = requests.get(url, headers=self.headers)
        resp_json = resp.json()

        return resp, resp_json

    def post(self, url, *, data):
        """
        Returns both the response and the json from the request.
        """

        resp = requests.post(url, data=data, headers=self.headers)
        resp_json = resp.json()

        return resp, resp_json

    def get_project_name_to_id_lookup(self) -> Dict[str, int]:
        """
        Get the lookup that maps the project name to the project id.
        """

        _, projects = self.get(self.projects_url)

        project_name_to_id_lookup: Dict[str, int] = {
            project['name']: project['id'] 
            for project in projects
        }

        return project_name_to_id_lookup

    def add_task(self, data):
        """
        Add a task to Todoist

        Example of `data`:
            data = {
                'content': 'Testing to Todoist 1'
                # 'project_id': int
                # priority
                # due_date
                # due_datetime
                # due_lang
                # label_ids
                # order
                # due string
            }

        TODO: I need to come up with a way to make these results composable as well. That way the
              user can choose how the review shows up in their task

              For example, do they want anything in the task as a comment? Or just a link that will 
              take them to the PR? For now, I will do the latter since it is easier.
        """

        _, new_task = self.post(self.tasks_url, data=data)

        return new_task
