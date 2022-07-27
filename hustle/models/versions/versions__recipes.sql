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
      , DATE(created_time) AS created_dt
      , DATE(last_edited_time) AS last_edited_dt
      , difficulty_level_id
      , cuisine_id
      , meal_type_id
      , url
      , object

FROM   `portfolio-351323.dev_tera.recipes`