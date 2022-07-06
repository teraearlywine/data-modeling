

  create or replace table `portfolio-351323`.`dbt_tera`.`staging__users`
  
  
  OPTIONS()
  as (
    


SELECT  RANK() OVER (PARTITION BY created_dt ORDER BY created_dt ASC) AS id
      , created_dt

FROM   `portfolio-351323`.`dbt_tera`.`staging__date`
  );
  