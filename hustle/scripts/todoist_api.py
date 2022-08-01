# Get my projects
from todoist_api_python.api import TodoistAPI 
import json
import pandas as pd
import requests


# Store in project config

url = "https://api.todoist.com/rest/v1/projects"
token = "6bdefb8d6b63fcbc3e74bcd0a155730386e5da87"

headers = {
    "Authorization": "Bearer " + token,
    "Accept": "application/json",
}

projects = requests.get(url, headers=headers)
data = projects.json()

json_export_file = "files/todoist_api.json"

with open(json_export_file, 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)

f.close()