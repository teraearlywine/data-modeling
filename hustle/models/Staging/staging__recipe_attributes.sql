{{
    config(
        materialized = "table"
    )
}}

SELECT  JSON_EXTRACT_SCALAR(attributes, '$.id') AS pk_attribute_id --one row for every color and attribute type
      , property_id
      , property_name
      , type
      , JSON_EXTRACT_SCALAR(attributes, '$.color') AS multi_select_color
      , JSON_EXTRACT_SCALAR(attributes, '$.name') AS attribute_type
      , attributes

FROM    {{ ref('versions__recipe_attributes') }}