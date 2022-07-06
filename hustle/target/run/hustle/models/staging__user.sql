

  create or replace view `portfolio-351323`.`dbt_tera`.`staging__user`
  OPTIONS()
  as 
-- TODO: 
-- find source data... or make my own? 

SELECT  ROW_NUMBER() OVER (PARTITION BY created_date) AS id
      , created_date

FROM (
        SELECT  GENERATE_DATE_ARRAY('1970-01-01', CURRENT_DATE, 1) AS created_date
        -- FROM    staging__user
);

