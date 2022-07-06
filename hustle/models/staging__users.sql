{{
    config(
        materialized = "table"
    )
}}


SELECT id
     , created_dt

FROM   {{ ref('staging__date') }}