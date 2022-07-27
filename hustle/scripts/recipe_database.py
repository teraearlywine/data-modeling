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

# # Create JSON file for viewing data structure
# json_export_file = "files/recipes_database.json"

# with open(json_export_file, 'w', encoding='utf8') as f:
#     json.dump(data, f, ensure_ascii=False)

all_recipes = []

for results in data['results']:
    current_recipe = []

    current_recipe.append(results['object'])
    current_recipe.append(results['id'])
    current_recipe.append(results['created_time'])
    current_recipe.append(results['last_edited_time'])
    current_recipe.append(results['properties']['Difficulty Level']['id'])  # difficulty level id
    current_recipe.append(results['properties']['Cuisine']['id'])           # cuisine id
    current_recipe.append(results['properties']['Meal Type']['id'])         # meal type id
    current_recipe.append(results['url'])

    all_recipes.append(current_recipe)


export_file = "files/recipes_database.csv"

with open(export_file, 'w') as fp:
    csv_w = csv.writer(fp, delimiter = ",")
    csv_w.writerows(all_recipes)

fp.close()

## Connect to MYSQL database

parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("recipes_mysql_config", "hostname")
port = parser.get("recipes_mysql_config", "port")
username = parser.get("recipes_mysql_config", "username")
# database = parser.get("recipes_mysql_config", "database")
password = parser.get("recipes_mysql_config", "password")

ms_conn = pymysql.connect(
          host = hostname
        , user = username
        , password = password
        # , database = database
        , port = int(port)
)

if ms_conn is None: 
    print("Error connecting to MySQL database")
else:
    print("MySQL connection established!")


# Transform CSV to dataframe 
mysql_db = pd.read_csv('files/recipes_database.csv', header=None)
mysql_db.columns = ['object', 'id', 'created_time', 'last_edited_time', 'difficulty_level_id', 'cuisine_id', 'meal_type_id' ,'url']

print(mysql_db.head())
# Create query that takes above data & inserts into recipes db
# query = ""
mysql_cursor = ms_conn.cursor()
mysql_cursor.execute('CREATE DATABASE IF NOT EXISTS meals;')

mysql_cursor.execute('CREATE TABLE IF NOT EXISTS meals.recipes(object VARCHAR(40), id VARCHAR(255), created_time VARCHAR(255), last_edited_time VARCHAR(255), difficulty_level_id VARCHAR(40), cuisine_id VARCHAR(40), meal_type_id VARCHAR(40), url VARCHAR(255));')
record = mysql_cursor.fetchone()

print("table is created")

for i,row in mysql_db.iterrows():
    sql = "INSERT INTO meals.recipes VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    mysql_cursor.execute(sql, tuple(row))
    print("Record inserted")

    ms_conn.commit()
mysql_cursor.close()
ms_conn.close()
# TO DO -- figure out how to convert the ISO8601 timestamp format
