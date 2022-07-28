{{
    config(
        materialized = "table"
    )
}}

-- create type 2 scd for recipes table
-- we want one row for each recipe + it's created date

WITH fields_cte AS (
            
    SELECT  recipe_id
          , created_dt
          , ARRAY_REVERSE(ARRAY_AGG(COALESCE(last_edited_dt, '1970-01-01') ORDER BY created_dt))[OFFSET(0)] AS last_edited_dt
          , ARRAY_REVERSE(ARRAY_AGG(COALESCE(url, 'NULL-PLACEHOLDER') ORDER BY created_dt))[OFFSET(0)] AS url
          , ARRAY_REVERSE(ARRAY_AGG(COALESCE(object, 'NULL-PLACEHOLDER') ORDER BY created_dt))[OFFSET(0)] AS object
    FROM    {{ ref('versions__recipes') }}
    GROUP BY 
          recipe_id
        , created_dt
      -- ORDER BY 
            -- created_dt ASC
) 

, start_end_cte AS (

    SELECT  * EXCEPT(created_dt)
          , created_dt AS effective_start_dt
          , DATE_SUB(LEAD(created_dt) OVER (PARTITION BY recipe_id ORDER BY created_dt), INTERVAL 1 DAY) AS effective_end_dt
    FROM   fields_cte

) 

, status_change_cte AS (

    SELECT  * 
          , IF(
                   LAG(last_edited_dt) OVER (PARTITION BY recipe_id ORDER BY effective_start_dt) != last_edited_dt
                OR LAG(url) OVER (PARTITION BY recipe_id ORDER BY effective_start_dt) != url
                OR LAG(object) OVER (PARTITION BY recipe_id ORDER BY effective_start_dt) != object
          , 1
          , 0
          ) AS has_status_changed
    FROM    start_end_cte

)

, ordinal_state_cte AS (

    SELECT  *
          , SUM(has_status_changed) OVER (PARTITION BY recipe_id ORDER BY effective_start_dt) AS ordinal_state
    FROM    status_change_cte

)

, first_last_cte AS (

    SELECT  *
          , FIRST_VALUE(effective_start_dt) OVER (PARTITION BY recipe_id, ordinal_state ORDER BY effective_start_dt) AS first_effective_start_dt
          , LAST_VALUE(effective_end_dt) OVER (PARTITION BY recipe_id, ordinal_state ORDER BY effective_start_dt RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_effective_end_dt
    FROM    ordinal_state_cte

)

SELECT DISTINCT 
      {{ dbt_utils.surrogate_key(['recipe_id', 'first_effective_start_dt']) }} AS pk_surrogate_key
      , NULLIF(recipe_id, 'NULL-PLACEHOLDER') AS recipe_id
      , NULLIF(url, 'NULL-PLACEHOLDER') AS url
      , NULLIF(object, 'NULL-PLACEHOLDER') AS object
      , NULLIF(last_edited_dt, '1970-01-01') AS last_edited_dt
      , first_effective_start_dt AS effective_start_dt 
      , last_effective_end_dt AS effective_end_dt
      , IF(last_effective_end_dt IS NULL, TRUE, FALSE) AS is_current
FROM  first_last_cte