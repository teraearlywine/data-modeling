import os 
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/teraearlywine/Dev/keys/portfolio-351323-80ace0374e30.json"

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "portfolio-351323.dev_tera.family_members"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("id", "INTEGER"),
        bigquery.SchemaField("first_name", "STRING"),
        bigquery.SchemaField("last_name", "STRING"),
        bigquery.SchemaField("created_ts", "TIMESTAMP"),
        bigquery.SchemaField("family_role", "STRING"),
    ],
    skip_leading_rows=0,
    # The source format defaults to CSV, so the line below is optional.
    # source_format=bigquery.SourceFormat.CSV,
)
uri = 'gs://data-pipeline12345/portfolio-351323'

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
print("Loaded {} rows.".format(destination_table.num_rows))