import requests
import json

url = "https://api.notion.com/v1/databases/16b28e43cf09487abad574ba0496da38/query"
token = "secret_3AsHcxtNxGOITtBY64iB8IaqvLi2jkPNQqbi3jI8bk5"


headers = {
    "Authorization": "Bearer " + token,
    "Accept": "application/json",
    "Notion-Version": "2022-06-28"
}

res = requests.post(url, headers=headers)
data = res.json()

json_export_file = "files/employement_database.json"
with open(json_export_file, 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)

