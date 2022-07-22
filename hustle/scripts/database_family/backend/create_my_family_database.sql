-- Active: 1657406218242@@127.0.0.1@3306
CREATE DATABASE IF NOT EXISTS my_people;

CREATE TABLE IF NOT EXISTS my_people.family (

    id INT AUTO_INCREMENT PRIMARY KEY
  , first_name VARCHAR(255) NOT NULL
  , last_name  VARCHAR(255) NOT NULL
  , created_ts TIMESTAMP NOT NULL 
  , family_role VARCHAR(255) NOT NULL

);

CREATE TABLE IF NOT EXISTS my_people.family_hobbies (

    id INT AUTO_INCREMENT PRIMARY KEY
  , hobby_type VARCHAR(255) NOT NULL
  , created_ts TIMESTAMP NOT NULL 
  , family_id INT
  , FOREIGN KEY(family_id) REFERENCES family(id)
);

CREATE TABLE IF NOT EXISTS my_people.family_birthdays (

    id INT AUTO_INCREMENT PRIMARY KEY
  , birthdate DATE NOT NULL
  , created_ts TIMESTAMP NOT NULL 

);




