### Steps to extract from MySQL db & load data to GCP


1. Run extract_mysql_incremental.py -- adds new rows to CSV files / GCP bucket
2. Run extract_mysql_full.py        -- extracts remainder table & adds to CSV files / GCP bucket
3. Run load_mysql_bq.py             -- loads GCP bucket data to new table

Currently there's an issue with appending, so I have to run the incremental first before the mysql full. 
The incremental script overwrites the full output.

The load job works, however I have to delete the table before running each of these. 
I anticipate will need some sort of append or merge thing.

TODO: 
- Figure out how to fix these things
- Write out API request pattern