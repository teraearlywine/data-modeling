

  create or replace view `portfolio-351323`.`dbt_tera`.`staging__date`
  OPTIONS()
  as 


WITH date_array_cte AS (

  SELECT  GENERATE_DATE_ARRAY('1970-01-01', CURRENT_DATE, INTERVAL 1 DAY) AS created_date

)

SELECT  x AS created_dt

FROM    date_array_cte
      , UNNEST(created_date) AS x;

