{{
    config(
        materialized = "table"
    )
}}

SELECT  fk_property_id AS pk_property_id
      , attribute_color
      , attribute_name 
FROM    {{ ref('dim__recipe_attributes') }}