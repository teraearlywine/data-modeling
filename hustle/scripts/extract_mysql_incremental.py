## Create mysql extraction script.
## $ python3 extract_mysql_incremental.py in terminal to execute

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

# Return newest data from family table

bq_sql = """SELECT COALESCE(MAX(DATE(created_ts)), '1900-01-01') FROM family;"""

# Creates new cursor to execute queries with
bq_cursor = conn.cursor()
bq_cursor.execute(bq_sql)

# Adds next row to result files
result = bq_cursor.fetchone()

# Upload first row & close cursor
last_updated_warehouse = result[0]
bq_cursor.close()

# Commits changes to stable storage
conn.commit()

## MySQL query
m_query = """SELECT * FROM family WHERE created_ts > %s;"""
local_filename = "files/family_extract.csv"

m_cursor = conn.cursor()
m_cursor.execute(m_query, last_updated_warehouse)
results = m_cursor.fetchall()

with open(local_filename, 'w', newline='') as fp:
    csv_w = csv.writer(fp, delimiter = ',')
    csv_w.writerows(results)

fp.close()
m_cursor.close()
conn.close()


# Load the GCP Credential values via parser
bucket_name = parser.get("gcp_config", "bucket_name")
source_file_name = parser.get("gcp_config", "source_file_name")
destination_blob_name = parser.get("gcp_config", "destination_blob_name")

# Upload to GCP 

# Create client instance
storage_client = storage.Client()
 
# Name of bucket to be instantiated
bucket = storage_client.bucket(bucket_name)

# Name of blob to be instantiated
blob = bucket.blob(destination_blob_name)

# Upload to bucket the configured source file name
blob.upload_from_filename(source_file_name)


print(f"File {source_file_name} uploaded to {destination_blob_name}.")
