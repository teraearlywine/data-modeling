from numpy import NaN, concatenate
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

created_ts = data["created_time"]

last_edited_ts = data["last_edited_time"]
index_placeholder = 1

results = [index_placeholder, created_ts, last_edited_ts]

print(results)

local_filename = "files/get_recipe_database_dates.csv"

with open(local_filename, 'w') as fp:
    csv_w = csv.writer(fp, delimiter = ',')
    csv_w.writerow(results)

fp.close()


# ## Connect to MYSQL database

parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("recipe_dates_mysql_config", "hostname")
port = parser.get("recipe_dates_mysql_config", "port")
username = parser.get("recipe_dates_mysql_config", "username")
password = parser.get("recipe_dates_mysql_config", "password")

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


# # Transform CSV to dataframe 
mysql_db = pd.read_csv('files/get_recipe_database_dates.csv', header=None)
mysql_db.columns = ['index_placeholder','created_ts', 'last_edited_ts']
mysql_db.set_index('index_placeholder')

# Create query that takes above data & inserts into recipes db
# query = ""
mysql_cursor = ms_conn.cursor()
mysql_cursor.execute('CREATE DATABASE IF NOT EXISTS meals;')

mysql_cursor.execute('CREATE TABLE IF NOT EXISTS meals.recipe_db_dates(index_placeholder  VARCHAR(100), created_ts VARCHAR(100), last_edited_ts VARCHAR(100));')
record = mysql_cursor.fetchone()

print("table is created")

for i,row in mysql_db.iterrows():
    sql = "INSERT INTO meals.recipe_db_dates VALUES (%s,%s,%s)"
    mysql_cursor.execute(sql, tuple(row))
    print("Record inserted")

    ms_conn.commit()

mysql_cursor.close()
ms_conn.close()