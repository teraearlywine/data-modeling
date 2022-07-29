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

WITH source_cte AS (

  SELECT DISTINCT id AS recipe_id
        , DATE(created_time) AS created_dt
        , DATE(last_edited_time) AS last_edited_dt
        , url
        , object
        , properties
  FROM   `portfolio-351323.dev_tera.recipes`

)

SELECT  * EXCEPT(properties)
        , [ JSON_EXTRACT_SCALAR(properties, '$.Difficulty Level.id') 
          , JSON_EXTRACT_SCALAR(properties, '$.Cuisine.id')
          , JSON_EXTRACT_SCALAR(properties, '$.Link.id') 
          , JSON_EXTRACT_SCALAR(properties, '$.Meal Type.id')
          , JSON_EXTRACT_SCALAR(properties, '$.Name.id')
          , JSON_EXTRACT_SCALAR(properties, '$.Created Time.id')
          , JSON_EXTRACT_SCALAR(properties, '$.Last Edited Time.id')
          ] AS properties_array
FROM    source_cte
