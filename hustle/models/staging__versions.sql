{{
    config(
        materialized = "table"
    )
}}


SELECT  id
      , name
      , created_dt
      , event_type

FROM   `portfolio-351323.dev_tera.versions`