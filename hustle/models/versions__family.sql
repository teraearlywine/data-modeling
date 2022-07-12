-- Active: 1657406218242@@127.0.0.1@3306@my_people
{{
    config(
        materialized="table"
    )
}}


SELECT  * 
FROM    my_people.family