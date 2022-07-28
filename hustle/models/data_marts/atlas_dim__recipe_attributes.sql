{{
    config(
        materialized = "table"
    )
}}


SELECT  ra.*
FROM    {{ ref('dim__recipe_attributes') }} AS ra
