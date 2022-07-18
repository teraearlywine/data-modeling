{{
    config(
        materialized = "view"
    )
}}

-- Person dimension, containing all the attributes of a given family member

SELECT  id
      , CONCAT(first_name, " ", last_name) AS full_name

FROM    {{ ref('staging__versions') }}