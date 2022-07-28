from numpy import NaN
import requests
import json
import csv
import pandas as pd
import configparser
import pymysql

url = "https://api.notion.com/v1/databases/2937358165574273b7802f26e528e634"
token = "secret_TAR6LEZxL4Uq8Am6gJi7L31II0smHMJQ33KQnQB5EWu"

headers = {
    "Authorization": "Bearer " + token,
    "Accept": "application/json",
    "Notion-Version": "2022-06-28"
}

res = requests.get(url, headers=headers)
data = res.json()
data = data["properties"]
json_export_file = "files/recipe_property_attributes.json"

with open(json_export_file, 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)

data = pd.read_json('files/recipe_property_attributes.json', orient="index")
data.to_csv("files/recipe_property_attributes.csv", index = False)




## connect to mysql database 

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
mysql_db = pd.read_csv('files/recipe_property_attributes.csv', header=0)
# Replace NaN & brackets with null placeholder values
# TO DO: figure out if there's a better way to iterate through rows

mysql_db['url'].fillna("NULL-PLACEHOLDER", inplace=True)
mysql_db['multi_select'].fillna("NULL-PLACEHOLDER", inplace=True)
mysql_db['title'].fillna("NULL-PLACEHOLDER", inplace=True)

mysql_db['url'].replace(to_replace="{}", value="NULL-PLACEHOLDER", inplace=True)
mysql_db['title'].replace(to_replace="{}", value="NULL-PLACEHOLDER", inplace=True)

mysql_db['created_time'].fillna("NULL-PLACEHOLDER", inplace=True)
mysql_db['created_time'].replace(to_replace="{}", value="NULL-PLACEHOLDER", inplace=True)

mysql_db['last_edited_time'].fillna("NULL-PLACEHOLDER", inplace=True)
mysql_db['last_edited_time'].replace(to_replace="{}", value="NULL-PLACEHOLDER", inplace=True)


# Create cursor
mysql_cursor2 = ms_conn.cursor()

# Create recipe attributes tbl
mysql_cursor2.execute('CREATE DATABASE IF NOT EXISTS meals;')
mysql_cursor2.execute('CREATE TABLE IF NOT EXISTS meals.recipe_attributes(id VARCHAR(40), name VARCHAR(255), type VARCHAR(255), created_time VARCHAR(255), last_edited_time VARCHAR(255), multi_select LONGTEXT, url VARCHAR(255), title VARCHAR(255));')
record = mysql_cursor2.fetchone()

print("table created!")

# Iterate over CSV, drop into new table
for i,row in mysql_db.iterrows():
    sql = "INSERT INTO meals.recipe_attributes VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    mysql_cursor2.execute(sql, tuple(row))
    print("Record inserted")

    ms_conn.commit()
mysql_cursor2.close()
ms_conn.close()