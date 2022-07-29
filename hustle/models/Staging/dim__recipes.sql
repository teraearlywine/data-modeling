{{
    config(
        materialized = "table"
    )
}}

-- create type 2 scd for recipes table
-- we want one row for each recipe + it's created date


WITH fields_cte AS (
            
    SELECT  recipe_id
          , last_edited_dt -- column that gets updated for changes to the page
          , ARRAY_REVERSE(ARRAY_AGG(COALESCE(created_dt, '1970-01-01') ORDER BY last_edited_dt))[OFFSET(0)] AS created_dt
          , ARRAY_REVERSE(ARRAY_AGG(COALESCE(url, 'NULL-PLACEHOLDER') ORDER BY last_edited_dt))[OFFSET(0)] AS url
          , ARRAY_REVERSE(ARRAY_AGG(COALESCE(object, 'NULL-PLACEHOLDER') ORDER BY last_edited_dt))[OFFSET(0)] AS object
    FROM    `portfolio-351323`.`dbt_tera`.`versions__recipes`
    GROUP BY 
          recipe_id
        , last_edited_dt
      ORDER BY 
            last_edited_dt ASC
)

-- inject a record for created time
, artificial_created_dt_version AS (

      SELECT  recipe_id
            , created_dt
            ,  * EXCEPT(row_num, recipe_id, created_dt)
      FROM (
            SELECT  *
                  , ROW_NUMBER() OVER (PARTITION BY recipe_id ORDER BY created_dt DESC) AS row_num
            FROM    fields_cte
            WHERE   created_dt <= COALESCE(last_edited_dt, CURRENT_DATE)
      )
      WHERE  row_num = 1
      AND    created_dt <= last_edited_dt
)

, map_artificial_version AS (

      SELECT  * 
      FROM    fields_cte

      UNION DISTINCT 

      SELECT  * 
      FROM    artificial_created_dt_version
)

, start_end_cte AS (

    SELECT  * --EXCEPT(created_dt)
          , last_edited_dt AS effective_start_dt
          , DATE_SUB(LEAD(last_edited_dt) OVER (PARTITION BY recipe_id ORDER BY last_edited_dt), INTERVAL 1 DAY) AS effective_end_dt
    FROM    map_artificial_version

) 

, status_change_cte AS (

    SELECT  * --EXCEPT(last_edited_dt)
          , IF(
                   LEAD(url) OVER (PARTITION BY recipe_id ORDER BY effective_start_dt) != url
                OR LEAD(created_dt) OVER (PARTITION BY recipe_id ORDER BY effective_end_dt) != created_dt
                OR LEAD(object) OVER (PARTITION BY recipe_id ORDER BY effective_start_dt) != object
                OR LEAD(last_edited_dt) OVER (PARTITION BY recipe_id ORDER BY effective_start_dt) != last_edited_dt
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

    SELECT  * EXCEPT(created_dt)
          , FIRST_VALUE(effective_start_dt) OVER (PARTITION BY recipe_id, ordinal_state ORDER BY effective_start_dt) AS first_effective_start_dt
          , LAST_VALUE(effective_end_dt) OVER (PARTITION BY recipe_id, ordinal_state ORDER BY effective_start_dt RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_effective_end_dt
    FROM    ordinal_state_cte

)

SELECT DISTINCT 
      {{ dbt_utils.surrogate_key(['recipe_id', 'first_effective_start_dt']) }} AS pk_surrogate_key
      , NULLIF(recipe_id, 'NULL-PLACEHOLDER') AS recipe_id
      , NULLIF(url, 'NULL-PLACEHOLDER') AS url
      , NULLIF(object, 'NULL-PLACEHOLDER') AS object
      -- , NULLIF(last_edited_dt, '1970-01-01') AS last_edited_dt
      , first_effective_start_dt AS effective_start_dt 
      , last_effective_end_dt AS effective_end_dt
      , IF(last_effective_end_dt IS NULL, TRUE, FALSE) AS is_current
FROM  first_last_cte