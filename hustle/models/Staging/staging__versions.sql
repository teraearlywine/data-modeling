{{
      config(
              materialized = "table"
            , partition_by = {
                    'field': 'created_dt'
                  , 'data_type': 'date'
                  , 'granularity': 'month' 
                  }
      )
}}

SELECT  id
      , first_name
      , last_name
      , DATE(created_ts) AS created_dt
      , family_role

FROM   `portfolio-351323.dev_tera.family_members`