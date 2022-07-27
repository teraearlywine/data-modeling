{{
    config(
        materialized = "table"
    )
}}

SELECT  *
FROM    {{ ref('versions__recipe_attributes') }}