

  create or replace view `portfolio-351323`.`dbt_tera`.`my_second_dbt_model`
  OPTIONS()
  as -- Use the `ref` function to select from other models

select *
from `portfolio-351323`.`dbt_tera`.`my_first_dbt_model`
where id = 1;

