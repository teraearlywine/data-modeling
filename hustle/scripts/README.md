### Steps to load data 


1. Run extract_mysql_incremental.py 
2. Run extract_mysql_full.py 
3. Run load_mysql_bq.py

Currently there's an issue with appending, so I have to run the incremental first before the mysql full. 
The incremental script overwrites the full output.

The load job works, however I have to delete the table before running each of these. 
I anticipate will need some sort of append or merge thing.