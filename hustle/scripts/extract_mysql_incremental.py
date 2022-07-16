## Create mysql extraction script.
## $ python3 extract_mysql_full.py in terminal to execute

import os
import pymysql
import csv
import configparser
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/teraearlywine/Dev/keys/portfolio-351323-80ace0374e30.json"


parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("mysql_config","hostname")
port = parser.get("mysql_config", "port")
username = parser.get("mysql_config", "username")
database = parser.get("mysql_config", "database")
password = parser.get("mysql_config", "password")

conn = pymysql.connect(host=hostname
      , user=username
      , password=password
      , database=database 
      , port=int(port)
)

if conn is None:
    print("Error connecting to the MySQL database")
else:
    print("MySQL Connection Established!")

bq_sql = "SELECT COALESCE(MAX(DATE(created_ts)), '1900-01-01') FROM family"
bq_cursor = conn.cursor()
bq_cursor.execute(bq_sql)
result = bq_cursor.fetchone()

# there's only one row & column returned
last_updated_warehouse = result[0]
bq_cursor.close()
bq_cursor.close()

m_query = "SELECT * FROM family WHERE created_ts > %s;"

local_filename = "files/family_extract.csv"

m_cursor = conn.cursor()
m_cursor.execute(m_query, (last_updated_warehouse,))
results = m_cursor.fetchall()

with open(local_filename, 'w') as fp:
    csv_w = csv.writer(fp, delimiter = ',')
    csv_w.writerows(results)
    fp.close()
    m_cursor.close()
    conn.close()


# Load the GCP Credential values
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
bucket_name = parser.get("gcp_config", "bucket_name")
source_file_name = parser.get("gcp_config", "source_file_name")
destination_blob_name = parser.get("gcp_config", "destination_blob_name")

# Upload to GCP 
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(source_file_name)


print(f"File {source_file_name} uploaded to {destination_blob_name}.")
