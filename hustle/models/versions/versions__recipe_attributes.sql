{{
    config(
         materialized = "table"
    )
}}

WITH source_cte AS (
    
  SELECT  id AS fk_property_id
        , name AS property_name
        , type
        , JSON_EXTRACT_ARRAY(PARSE_JSON(REPLACE(NULLIF(multi_select, 'NULL-PLACEHOLDER'), "'", '"')), "$.options") AS attributes_array
  FROM   `portfolio-351323.dev_tera.recipe_attributes`

)

SELECT  * EXCEPT(attributes_array, attributes)
      , JSON_EXTRACT_SCALAR(attributes, '$.id') AS pk_attribute_id
      , JSON_EXTRACT_SCALAR(attributes, '$.color') AS attribute_color
      , JSON_EXTRACT_SCALAR(attributes, '$.name') AS attribute_name
FROM    source_cte

        CROSS JOIN UNNEST(attributes_array) AS attributes
