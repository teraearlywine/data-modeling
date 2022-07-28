{{
    config(
        materialized = "table"
    )
}}

SELECT  recipe_id
      , created_dt 
      , last_edited_dt
      , url
      , object
      , fk_property_id
FROM    {{ ref('versions__recipes') }}