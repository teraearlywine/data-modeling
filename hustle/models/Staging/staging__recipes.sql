{{
    config(
        materialized = "table"
    )
}}

SELECT  recipe_id
      , created_dt
      , last_edited_dt
      , difficulty_level_id
      , cuisine_id
      , meal_type_id
      , url
      , object

FROM    {{ ref('versions__recipes') }}