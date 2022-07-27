import os
import configparser
from google.cloud import bigquery

parser = configparser.ConfigParser()
parser.read("pipeline.conf")

local_gcp_cred = parser.get("food_gcp_config", "local_gcp_cred")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = local_gcp_cred

# Init BQ client

client = bigquery.Client()
table_id = "portfolio-351323.dev_tera.recipe_attributes"

job_config = bigquery.LoadJobConfig(
    schema=[
          bigquery.SchemaField("id", "STRING")
        , bigquery.SchemaField("name", "STRING")
        , bigquery.SchemaField("type","STRING")
        , bigquery.SchemaField("multi_select", "STRING")
        , bigquery.SchemaField("url","STRING")
        , bigquery.SchemaField("title","STRING")
    ]
)

uri = 'gs://data-pipeline12345/recipe_attributes_db'

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)