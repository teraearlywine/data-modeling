import os
import pymysql
import csv
import configparser
from google.cloud import storage

parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("food_mysql_config", "hostname")
port = parser.get("food_mysql_config", "port")
username = parser.get("food_mysql_config", "username")
database = parser.get("food_mysql_config", "database")
password = parser.get("food_mysql_config", "password")

ms_conn = pymysql.connect(
      host=hostname
    , user=username
    , password=password
    , database=database
    , port=int(port)
)

if ms_conn is None: 
    print("Error connecting to mysql database")
else: 
    print("MySQL connection established!")

query = "SELECT * FROM meals.recipe_attributes"
local_filename = "files/recipe_attributes_extract.csv"

cursor = ms_conn.cursor()
cursor.execute(query)
results = cursor.fetchall()

with open(local_filename, 'w') as fp:
    csvw = csv.writer(fp, delimiter = ",")
    csvw.writerows(results)
fp.close()
cursor.close()
ms_conn.close()

## Connect to GCP

bucket_name = parser.get("food_gcp_config", "bucket_name")
source_file_name = parser.get("food_gcp_config", "source_file_name2")
destination_blob_name = parser.get("food_gcp_config", "destination_blob_name2")
local_gcp_cred = parser.get("food_gcp_config", "local_gcp_cred")

# Connect to credentials 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = local_gcp_cred

# Init storage client
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(source_file_name)

print(f"File {source_file_name} uploaded to {destination_blob_name}.")