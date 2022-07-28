{{
    config(
        materialized = "table"
    )
}}

SELECT  pk_attribute_id --one row for every color and attribute type
      , fk_property_id
      , property_name
      , type
      , attribute_color
      , attribute_name
FROM    {{ ref('versions__recipe_attributes') }}