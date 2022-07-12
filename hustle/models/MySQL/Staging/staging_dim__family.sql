-- Modeling family data for interview practice

SELECT  id
      , first_name
      , last_name
      , created_ts
      , family_role
      , IF(family_role IN ('Father', 'Mother', 'Grand Mother'), 1, 0) AS is_parent
      
FROM    family