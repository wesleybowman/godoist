"""
A test to see if I could create a task in my Todoist
"""
import json
import requests
import uuid

from config import config

HEADERS = {
    "Authorization": f"Bearer {config['TODOIST_API_TOKEN']}",
    "Content-Type": "application/json",
    # What is `X-Request-Id`: https://stackoverflow.com/a/27174552/1141389
    "X-Request-Id": str(uuid.uuid4()),
}

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

url = "https://beta.todoist.com/API/v8/tasks"
resp = requests.post(url, data=json.dumps(data), headers=HEADERS)
resp_json = resp.json()
