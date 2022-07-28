{{
    config(
        materialized = "table"
    )
}}

SELECT  * 
FROM    {{  ref('dim__recipe_attributes')   }}