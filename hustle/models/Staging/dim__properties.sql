{{
    config(
        materialized = "table"
    )
}}

SELECT  property_id
      , attribute_color
      , attribute_name 
FROM    {{ ref('dim__recipe_attributes') }}