import requests
import json
import csv
import pymysql
import configparser
import pandas as pd

url = "https://api.notion.com/v1/databases/2937358165574273b7802f26e528e634/query"
token = "secret_TAR6LEZxL4Uq8Am6gJi7L31II0smHMJQ33KQnQB5EWu"

headers = {
    "Authorization": "Bearer " + token,
    "Accept": "application/json",
    "Notion-Version": "2022-06-28"
}

# For POST api calls in notion, in the URL you need a /query 
# For GET api calls you don't.

res = requests.post(url, headers=headers)
data = res.json()

# Create JSON file for viewing data structure
json_export_file = "files/recipes_database_full.json"

with open(json_export_file, 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)

f.close()