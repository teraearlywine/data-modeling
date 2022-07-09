
## This is just a text file to highlight the SQL I used to create my play modeling data. 

DBT doesn't support DDL statements, all operations were completed in BQ

```
CREATE TABLE IF NOT EXISTS dbt_tera.versions (
    id         STRING 
  , name       STRING NOT NULL
  , created_dt DATE NOT NULL
  , event_type STRING NOT NULL
);
```

```
INSERT INTO dbt_tera.versions(id, name, created_dt, event_type)

VALUES
        (GENERATE_UUID(), 'Tera', CURRENT_DATE, 'CoolPersonA')
      , (GENERATE_UUID(), 'David', CURRENT_DATE, 'CoolPersonB')
;
```