{{
    config(
         materialized = "table"
    )
}}

WITH source_cte AS (
    
  SELECT  id AS property_id
        , name AS property_name
        , type
        , JSON_EXTRACT_ARRAY(PARSE_JSON(REPLACE(NULLIF(multi_select, 'NULL-PLACEHOLDER'), "'", '"')), "$.options") AS options_array
  FROM   `portfolio-351323.dev_tera.recipe_attributes`

)

SELECT  * EXCEPT(options_array)
FROM    source_cte

        CROSS JOIN UNNEST(options_array) AS attributes
