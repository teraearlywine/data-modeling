import os
import configparser
from google.cloud import bigquery

parser = configparser.ConfigParser()
parser.read("pipeline.conf")

local_gcp_cred = parser.get("food_gcp_config", "local_gcp_cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = local_gcp_cred

# Initialize a BQ client 

client = bigquery.Client()
table_id = "portfolio-351323.dev_tera.recipe_dates"

# Config job & set schema
job_config = bigquery.LoadJobConfig(
     schema=[
        bigquery.SchemaField("index_placeholder", "STRING"),
        bigquery.SchemaField("created_ts", "STRING"),
        bigquery.SchemaField("last_edited_ts", "STRING"),
     ]
)

# Bucket path to grab data from
uri = 'gs://data-pipeline12345/recipe_dates_bucket'


# Make API request
load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)