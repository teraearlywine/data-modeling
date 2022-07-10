-- Active: 1657406218242@@127.0.0.1@3306@my_people

CREATE PROCEDURE 
    add_new_member (
          IN first_name VARCHAR(255) 
        , IN last_name  VARCHAR(255) 
        , IN created_ts TIMESTAMP 
        , IN family_role VARCHAR(255)
    )

BEGIN

    INSERT INTO family(first_name, last_name, created_ts, family_role)
    VALUES(first_name, last_name, created_ts, family_role);

END