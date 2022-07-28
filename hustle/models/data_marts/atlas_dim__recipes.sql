{{
    config(
        materialized = "table"
    )
}}

SELECT  pk_surrogate_key
      , recipe_id
      , url
      , object
      , last_edited_dt
      , effective_start_dt
      , effective_end_dt
      , is_current
FROM    {{ ref('dim__recipes') }}