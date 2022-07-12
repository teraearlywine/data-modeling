-- Modeling family data for interview practice

WITH 

family_cte AS (
            
      SELECT  id
            , first_name
            , last_name
            , created_ts
            , family_role
            , CASE WHEN family_role IN ('Daughter', 'Sister', 'Boyfriend') THEN 'child'
                   WHEN family_role IN ('Father', 'Mother') THEN 'parent'
                   ELSE NULL END AS nuclear_hierarchy
            , IF(last_name IN ("Earlywine", "Manning"), 0, 1) AS is_grim

      FROM    family

)
-- inject artificial parents version
-- create primary key representing parent_id
, parent_version_cte AS (
      SELECT  c.* 
            , p.id AS parent_id
      FROM (
                  SELECT  p.id
                  FROM    family_cte AS p 
                  WHERE   p.nuclear_hierarchy = "parent"
                  
            ) AS p

      RIGHT JOIN family_cte AS c 
            ON  p.id = c.id

) 

SELECT  * 
FROM    parent_version_cte