

WITH 
  
date_array_cte AS (

    SELECT  GENERATE_DATE_ARRAY('1970-01-01', CURRENT_DATE, INTERVAL 1 DAY) AS created_date

)

, date_cte AS (

    SELECT  x AS created_dt
          , RANK() OVER (ORDER BY x ASC) AS id
    FROM    date_array_cte, UNNEST(created_date) AS x 

)


SELECT  id
      , created_dt

FROM    date_cte

  