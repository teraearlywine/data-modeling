{{
    config(
        materialized = "table"
    )
}}

SELECT  ra.* 
    --   , r.recipe_id AS fk_recipe_id
    --   , r.url AS recipe_url
FROM    {{ ref('versions__recipe_attributes') }} AS ra

        -- INNER JOIN {{ ref('versions__recipes') }} AS r
        --     ON ra.fk_property_id = r.fk_property_id