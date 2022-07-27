{{
    config(
        materialized = "table"
    )
}}

SELECT  *
FROM    {{ ref('versions__recipes') }}