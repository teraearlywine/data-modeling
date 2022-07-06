

  create or replace table `portfolio-351323`.`dbt_tera`.`staging__users`
  
  
  OPTIONS()
  as (
    


SELECT id
     , created_dt

FROM   `portfolio-351323`.`dbt_tera`.`staging__date`
  );
  