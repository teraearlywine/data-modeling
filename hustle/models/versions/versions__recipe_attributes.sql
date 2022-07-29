{{
    config(
         materialized = "table"
    )
}}

WITH source_cte AS (

  SELECT DISTINCT id AS property_id
        , name AS property_name
        , type
        , created_time
        , last_edited_time
        , multi_select
  FROM   `portfolio-351323.dev_tera.recipe_attributes`

)

SELECT  * EXCEPT(multi_select)
      , PARSE_JSON(REPLACE(NULLIF(multi_select, 'NULL-PLACEHOLDER'), "'", '"')) AS attributes_json

FROM    source_cte