"""
A test to see if I could create a task in my Todoist
"""
import json
import requests
import uuid
from typing import Dict

from config import config

HEADERS = {
    "Authorization": f"Bearer {config['TODOIST_API_TOKEN']}",
    "Content-Type": "application/json",
    # What is `X-Request-Id`: https://stackoverflow.com/a/27174552/1141389
    "X-Request-Id": str(uuid.uuid4()),
}

url = "https://beta.todoist.com/API/v8/projects"
resp = requests.get(url, headers=HEADERS)
projects = resp.json()

project_name_to_id_lookup: Dict[str, int] = {project['name']: project['id'] for project in projects}
