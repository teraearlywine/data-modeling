import os
import pymysql
import csv
import configparser
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/teraearlywine/Dev/keys/portfolio-351323-80ace0374e30.json"

## Configure MySQL connection using parser

parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("food_mysql_config", "hostname")
port = parser.get("food_mysql_config", "port")
username = parser.get("food_mysql_config", "username")
database = parser.get("food_mysql_config", "database")
password = parser.get("food_mysql_config", "password")

## Set config file to pymysql connection

ms_conn = pymysql.connect(
          host=hostname
        , user=username
        , password=password
        , database=database
        , port=int(port)
)

if ms_conn is None: 
    print("Error connecting to the MySQL database")
else: 
    print("MySQL connection established!")


query = "SELECT * FROM recipes"
local_filename = "files/recipes_extract.csv"

# Create new cursor to execute query

r_cursor = ms_conn.cursor()
r_cursor.execute(query)
results = r_cursor.fetchall()

# Write to local_filename as a CSV file

with open(local_filename, 'w') as fp:
    csv_w = csv.writer(fp, delimiter = ',')
    csv_w.writerows(results)

# End script by closing write statement, SQL execution and connection to db

fp.close()
r_cursor.close()
ms_conn.close()


### Part two: load to GCP storage bucket

# Use parser to load credentials

bucket_name = parser.get("food_gcp_config", "bucket_name")
source_file_name = parser.get("food_gcp_config", "source_file_name")
destination_blob_name = parser.get("food_gcp_config", "destination_blob_name")

# Upload to GCP 

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(source_file_name)

print(f"File {source_file_name} uploaded to {destination_blob_name}.")